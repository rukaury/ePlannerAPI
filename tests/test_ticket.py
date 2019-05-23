from tests.base import BaseTestCase
import unittest
import json

class TestTicket(BaseTestCase):

    def create_ticket(self, token):
        """
        Create a ticket into an event
        :param token:
        :return:
        """
        response = self.client.post(
            'v1/events/1/tickets/1',
            data=json.dumps(dict(ticket= dict(qr_code='qrcodetext', vvip='0', accepted='0', scanned='0', comments='Test'))),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )
        data = json.loads(response.data.decode())        
        self.assertEqual(data['ticket']['ticket_id'], 1)
        self.assertEqual(data['ticket']['event_id'], 1)
        self.assertEqual(data['ticket']['guest_id'], 1)
        self.assertTrue(data['ticket']['qr_code'] == 'qrcodetext')
        self.assertTrue(data['ticket']['vvip'] == False)
        self.assertTrue(data['ticket']['accepted'] == False)
        self.assertEqual(data['ticket']['scanned'], 0)
        self.assertTrue(data['ticket']['comments'] == 'Test')
        self.assertTrue(data['status'] == 'success')
        self.assertEqual(response.status_code, 200)
        

    def create_tickets(self, token):
        """
        Create a ticket into an event
        :param token:
        :return:
        """
        tickets = [
            {'ticket': {'qr_code':'qrcodetext', 'vvip':'0', 'accepted':'1', 'scanned':'1', 'comments':'Test'}},
            {'ticket': {'qr_code':'textqrcode', 'vvip':'1', 'accepted':'0', 'scanned':'2', 'comments':'Test1'}},
            {'ticket': {'qr_code':'qrtextcode', 'vvip':'0', 'accepted':'1', 'scanned':'3', 'comments':'Test2'}},
            {'ticket': {'qr_code':'codetextqr', 'vvip':'1', 'accepted':'0', 'scanned':'4', 'comments':'Test3'}},
            {'ticket': {'qr_code':'codeqrtext', 'vvip':'0', 'accepted':'1', 'scanned':'5', 'comments':'Test4'}},
            {'ticket': {'qr_code':'textcodeqr', 'vvip':'1', 'accepted':'0', 'scanned':'6', 'comments':'Test5'}},
            {'ticket': {'qr_code':'qrcodetextqrcodetext', 'vvip':'0', 'accepted':'1', 'scanned':'7', 'comments':'Test6'}},
        ] 

        for i in range(1, len(tickets) + 1):
            response = self.client.post(
                'v1/events/1/tickets/' + str(i),
                data=json.dumps(dict(ticket=dict(qr_code=tickets[i - 1]['ticket']['qr_code'], vvip=tickets[i - 1]['ticket']['vvip'], accepted=tickets[i - 1]['ticket']['accepted'], scanned=tickets[i - 1]['ticket']['scanned'], comments=tickets[i - 1]['ticket']['comments']))),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['ticket']['qr_code'] == tickets[i - 1]['ticket']['qr_code'])
            self.assertTrue(data['ticket']['vvip'] == False or data['ticket']['vvip'] == True)
            self.assertTrue(data['ticket']['accepted'] == False or data['ticket']['accepted'] == True)
            self.assertEqual(data['ticket']['scanned'], i)
            self.assertEqual(data['ticket']['event_id'], 1)
            self.assertEqual(data['ticket']['guest_id'], i)
            self.assertTrue(data['ticket']['comments'] == tickets[i - 1]['ticket']['comments'])
            self.assertEqual(response.status_code, 200)

    def test_ticket_post_request_content_type(self):
        """
        Test that the correct response is returned if the request payload content type is not application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/events/1/tickets/1',
                data=json.dumps(dict(ticket= dict(qr_code='qrcodetext', vvip='0', accepted='0', scanned='0', comments='Test'))),
                content_type='application/javascript',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be application/json')
            self.assertEqual(response.status_code, 401)

    def test_ticket_put_request_content_type(self):
        """
        Test that the correct response is returned if the request payload content type is not application/json
        :return:
        """
        with self.client:
            response = self.client.put(
                'v1/events/1/tickets/1',
                data=json.dumps(dict(ticket= dict(qr_code='qrcodetext'))),
                content_type='application/javascript',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be application/json')
            self.assertEqual(response.status_code, 401)

    def test_event_id_is_invalid_in_post_request(self):
        """
        Test that the event Id is invalid
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/events/id/tickets/1',
                data=json.dumps(dict(ticket= dict(qr_code='qrcodetext'))),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid Event Id')
            self.assertEqual(response.status_code, 401)

    def test_event_id_is_invalid_in_put_request(self):
        """
        Test that the event Id is invalid
        :return:
        """
        with self.client:
            response = self.client.put(
                'v1/events/id/tickets/1',
                data=json.dumps(dict(ticket= dict(qr_code='qrcodetext'))),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid Event Id')
            self.assertEqual(response.status_code, 401)

    def test_qrcode_attribute_is_missing_in_post_request(self):
        with self.client:
            response = self.client.post(
                'v1/events/1/tickets/1',
                data=json.dumps(dict(ticket=dict(comments=''))),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Missing some ticket attribute(s), nothing has changed.')
            self.assertEqual(response.status_code, 401)

    def test_some_attribute_is_missing_in_put_request(self):
        """
        Test some attribute are missing
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            self.create_guest(token)
            self.create_ticket(token)
            response = self.client.put(
                'v1/events/1/tickets/1',
                data=json.dumps(dict(ticket=dict())),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Missing some ticket attribute(s), nothing has changed.')
            self.assertEqual(response.status_code, 401)


    def test_correct_response_when_user_has_no_event_with_specified_id_post_request(self):
        """
        Test that a user does not have an event specified by that Id
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/events/1/tickets/1',
                data=json.dumps(dict(ticket= dict(qr_code='qrcodetext', vvip='0', accepted='0', scanned='0', comments='Test'))),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'User has no event with Id 1')
            self.assertEqual(response.status_code, 202)

    def test_correct_response_when_user_has_no_event_with_specified_id_get_request(self):
        """
        Test that a user does not have a event specified by that Id
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/events/1/tickets',
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Event not found')
            self.assertEqual(response.status_code, 404)

    def test_a_ticket_has_been_successfully_saved(self):
        """
        Test an Event ticket has been successfully stored.
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            self.create_guest(token)
            self.create_ticket(token)


    def test_tickets_are_returned(self):
        """
        Test Event tickets are returned and the tickets are in a list
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            self.create_guest(token)
            self.create_ticket(token)
            response = self.client.get(
                'v1/events/1/tickets',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['tickets'], list, 'Items must be a list')
            self.assertEqual(len(data['tickets']), 1)
            self.assertEqual(data['count'], 1)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], None)
            self.assertEqual(response.status_code, 200)

    def test_tickets_returned_when_searched(self):
        """
        Test Event tickets are returned when a query search q is present in the url
        Also test that the next page pagination string is 'http://localhostv1/events/1/tickets/?page=2'
        and previous is none
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            self.create_guests(token)
            self.create_tickets(token)
            response = self.client.get(
                'v1/events/1/tickets?q=qr',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['tickets'], list, 'Items must be a list')
            self.assertEqual(len(data['tickets']), 4)
            self.assertEqual(data['tickets'][0]['event_id'], 1)
            self.assertEqual(data['tickets'][0]['guest_id'], 7)
            self.assertEqual(data['tickets'][0]['ticket_id'], 7)
            self.assertEqual(data['count'], 7)
            self.assertEqual(data['next'], 'http://localhost/v1/events/1/tickets?q=qr&page=2')
            self.assertEqual(data['previous'], None)
            self.assertEqual(response.status_code, 200)

    def test_tickets_returned_when_searched_2(self):
        """
        Test Event tickets are returned when a query search q is present in the url
        Also test that the next page pagination is none and previous 'http://localhostv1/events/1/tickets?page=1'
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            self.create_guests(token)
            self.create_tickets(token)
            response = self.client.get(
                'v1/events/1/tickets?q=qr&page=2',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['tickets'], list, 'Items must be a list')
            self.assertEqual(len(data['tickets']), 3)
            self.assertEqual(data['tickets'][0]['event_id'], 1)
            self.assertEqual(data['tickets'][0]['guest_id'], 3)
            self.assertEqual(data['tickets'][0]['ticket_id'], 3)
            self.assertEqual(data['count'], 7)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], 'http://localhost/v1/events/1/tickets?q=qr&page=1')
            self.assertEqual(response.status_code, 200)


    def test_empty_ticket_list_is_returned_when_no_tickets_in_event(self):
        """
        Test empty tickets list is returned when the event is empty
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            response = self.client.get(
                'v1/events/1/tickets',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_ticket_is_returned_successfully_get_request(self):
        """
        Test a ticket is returned on a get request
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            self.create_guest(token)
            self.create_ticket(token)
            response = self.client.get(
                'v1/events/1/tickets/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(data['ticket']['ticket_id'], 1)
            self.assertEqual(response.status_code, 200)

    def test_ticket_to_be_returned_on_get_request_does_not_exist(self):
        """
        Test that the ticket to be returned on a get request does not exist.
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            response = self.client.get(
                'v1/events/1/tickets/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'ticket not found')
            self.assertEqual(response.status_code, 404)

    def test_invalid_ticket_id_get_one_ticket_request(self):
        """
        Test that an invalid ticket Id has been sent to get an ticket
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/events/1/tickets/dsfdgfghjg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid ticket Id')
            self.assertEqual(response.status_code, 202)


    def test_no_event_on_get_ticket_request(self):
        """
        Test there is no Event specified by that Id when getting an ticket by Id
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/events/1/tickets/1',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'User has no event with Id 1')
            self.assertEqual(response.status_code, 404)

    def test_invalid_ticket_id_delete_request(self):
        """
        Test that an invalid ticket Id has been sent.
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/events/1/tickets/dsfdgfghjg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid ticket Id')
            self.assertEqual(response.status_code, 202)

    def test_no_event_delete_request(self):
        """
        Test there is no Event specified by that Id
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/events/1/tickets/1',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'User has no event with Id 1')
            self.assertEqual(response.status_code, 202)

    def test_ticket_is_deleted_successfully(self):
        with self.client:
            token = self.get_user_token()
            self.create_event(token)
            self.create_guest(token)
            self.create_ticket(token)
            response = self.client.delete(
                'v1/events/1/tickets/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully deleted the ticket from event with Id 1')
            self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()