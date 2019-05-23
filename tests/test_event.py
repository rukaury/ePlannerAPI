from tests.base import BaseTestCase
import unittest
import json


class TestEventBluePrint(BaseTestCase):
    def test_creating_an_event(self):
        """
        Test that a user can add an event
        :return:
        """
        with self.client:
            self.create_event(self.get_user_token())

    def test_missing_attributes_is_set_in_event_creation_request(self):
        """
        Test that some attribute are present in the json request.
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/events/',
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                data=json.dumps({"event":{}}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Missing some event data, nothing was changed')

    def test_event_post_content_type_is_json(self):
        """
        Test that the request content type is application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/events/',
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                data=json.dumps(dict(event = dict(name = "Some Event", location="7 Bayview yards", time = "2019-05-22 10:00:00", eval_link="http://google.ca")))
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Content-type must be json')

    def test_user_can_get_list_of_events(self):
        """
        Test that a user gets back a list of their events or an empty dictionary if they do not have any yet
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/events/',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['events'], list)
            self.assertEqual(len(data['events']), 0)
            self.assertEqual(data['count'], 0)
            self.assertIsInstance(data['count'], int)
            self.assertEqual(data['previous'], None)
            self.assertEqual(data['next'], None)

    def test_request_for_an_event_has_integer_id(self):
        """
        Test that only integer event Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/events/dsfgsdsg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Event Id')

    def test_event_by_id_is_returned_on_get_request(self):
        """
        Test that a user event is returned when a specific Id is specified
        :return:
        """
        with self.client:
            token = self.get_user_token()
            # Create a Event
            response = self.client.post(
                'v1/events/',
                data=json.dumps(dict(event = dict(name = "Some Event", location="7 Bayview yards", time = "2019-05-22 10:00:00", eval_link="http://google.ca"))),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Event creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['event_name'], 'Some Event')
            self.assertTrue(data['event']['event_location'], '7 Bayview yards')
            self.assertTrue(data['event']['event_time'], '2019-05-22 10:00:00')
            self.assertTrue(data['event']['event_eval_link'], 'http://google.ca')
            response = self.client.get(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['event_name'], 'Some Event')
            self.assertTrue(data['event']['event_location'], '7 Bayview yards')
            self.assertTrue(data['event']['event_time'], '2019-05-22 10:00:00')
            self.assertTrue(data['event']['event_eval_link'], 'http://google.ca')
            self.assertIsInstance(data['event'], dict)
            self.assertTrue(response.content_type == 'application/json')

    def test_no_event_returned_by_given_id(self):
        """
        Test there is no event/no event returned with given Id
        :return:
        """
        with self.client:
            token = self.get_user_token()

            response = self.client.get(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Event not found')
            self.assertTrue(response.content_type == 'application/json')

    def test_deletion_handles_no_event_found_by_id(self):
        """
        Show that a 404 response is returned when an un existing event is being deleted.
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Event resource cannot be found')
            self.assertTrue(response.content_type == 'application/json')

    def test_request_for_deleting_event_has_integer_id(self):
        """
        Test that only integer event Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/events/dsfgsdsg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Event Id')

    def test_event_is_updated(self):
        """
        Test that the Event details(name) is updated
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()

            # Create a Event
            response = self.client.post(
                'v1/events/',
                data=json.dumps(dict(event = dict(name = "Some Event", location="7 Bayview yards", time = "2019-05-22 10:00:00", eval_link="http://google.ca"))),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )

            # Test Event creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['event_name'], 'Some Event')
            self.assertTrue(data['event']['event_location'], '7 Bayview yards')
            self.assertTrue(data['event']['event_time'], '2019-05-22 10:00:00')
            self.assertTrue(data['event']['event_eval_link'], 'http://google.ca')

            # Update the event name
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(name = "Manion Lecture"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['event_name'], 'Manion Lecture')
            self.assertEqual(data['event']['event_id'], 1)

            # Update the event location
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(location = "363 Sussex Dr, Ottawa, ON"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['event_location'], '363 Sussex Dr, Ottawa, ON')
            self.assertEqual(data['event']['event_id'], 1)

            # Update the event time
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(time = "2020-08-09 22:00:30"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['event_time'], '2020-08-09 22:00:30')
            self.assertEqual(data['event']['event_id'], 1)

    def test_id_of_event_to_be_edited_does_not_exist(self):
        """
        Test the event to be updated does not exist.
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            # Update the event name
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(name = "Manion Event"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 404)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'The Event with Id 1 does not exist')

    def test_id_of_event_to_be_edited_is_invalid(self):
        """
        Test the event id is invalid.
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            # Update the event name
            res = self.client.put(
                'v1/events/eventid',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(name = "Manion Event", location="7 Bayview yards", time = "2019-05-22 10:00:00", eval_link="http://google.ca"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Event Id')

    def test_content_type_for_editing_event_is_json(self):
        """
        Test that the content type used for the request is application/json
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(name = "Some Event", location="7 Bayview yards", time = "2019-05-22 10:00:00", eval_link="http://google.ca")))
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 202)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be json')

    def test_required_event_name_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(name) exists and has value in the request payload
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(name = ""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_required_event_location_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(location) exists and has value in the request payload
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(location=""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_required_event_time_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(time) exists and has value in the request payload
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(event = dict(time = ""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_event_is_deleted(self):
        """
        Test that a Event is deleted successfully
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            response = self.client.post(
                'v1/events/',
                data=json.dumps(dict(event = dict(name = "Manion event", location="7 Bayview yards", time = "2019-05-22 10:00:00", eval_link="http://google.ca"))),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Event creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['event_name'], 'Manion event')
            self.assertTrue(data['event']['event_location'], '7 Bayview yards')
            self.assertTrue(data['event']['event_time'], '2019-05-22 10:00:00')
            self.assertTrue(data['event']['event_eval_link'], 'http://google.ca')
            # Delete the created Event
            res = self.client.delete(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Event Deleted successfully')
            self.assertTrue(res.content_type == 'application/json')

    def test_400_bad_requests(self):
        """
        Test for Bad requests - 400s
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/events/1',
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Bad Request')

    def test_events_returned_when_searched(self):
        """
        Test Events are returned when a query search q is present in the url
        Also test that the next page pagination string is 'http://localhost/events/1/items/?page=2'
        and previous is none
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_events(token)
            response = self.client.get(
                'v1/events/?q=T',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['events'], list, 'Items must be a list')
            self.assertEqual(len(data['events']), 4)
            self.assertEqual(data['events'][0]['event_id'], 1)
            self.assertEqual(data['count'], 6)
            self.assertEqual(data['next'], 'http://localhost/v1/events/?q=T&page=2')
            self.assertEqual(data['previous'], None)
            self.assertEqual(response.status_code, 200)

    def test_events_returned_when_searched_2(self):
        """
        Test Events are returned when a query search q is present in the url
        Also test that the next page pagination string is None
        and previous is 'http://localhost/events/1/items/?page=1'
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_events(token)
            response = self.client.get(
                'v1/events/?q=T&page=2',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['events'], list, 'Items must be a list')
            self.assertEqual(len(data['events']), 2)
            self.assertEqual(data['events'][0]['event_id'], 5)
            self.assertEqual(data['count'], 6)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], 'http://localhost/v1/events/?q=T&page=1')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
