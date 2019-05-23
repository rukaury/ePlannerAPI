from tests.base import BaseTestCase
import unittest
import json


class TestGuestBluePrint(BaseTestCase):
    def test_creating_a_guest(self):
        """
        Test that a user can add a guest
        :return:
        """
        with self.client:
            self.create_guest(self.get_user_token())

    def test_missing_attributes_is_set_in_guest_creation_request(self):
        """
        Test that some attribute are present in the json request.
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/guests/',
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                data=json.dumps({"guest":{}}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Missing some guest data, nothing was changed')

    def test_guest_post_content_type_is_json(self):
        """
        Test that the request content type is application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/guests/',
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                data=json.dumps(dict(guest = dict(first_name = "Tim", last_name="Hortons", organization = "TIMS", email="tim.hortons@tims.ca")))
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Content-type must be json')

    def test_user_can_get_list_of_guests(self):
        """
        Test that a user gets back a list of their guests or an empty dictionary if they do not have any yet
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/guests/',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['guests'], list)
            self.assertEqual(len(data['guests']), 0)
            self.assertEqual(data['count'], 0)
            self.assertIsInstance(data['count'], int)
            self.assertEqual(data['previous'], None)
            self.assertEqual(data['next'], None)

    def test_request_for_a_guest_has_integer_id(self):
        """
        Test that only integer guest Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/guests/dsfgsdsg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Guest Id')

    def test_guest_by_id_is_returned_on_get_request(self):
        """
        Test that a user guest is returned when a specific Id is specified
        :return:
        """
        with self.client:
            token = self.get_user_token()
            # Create a Guest
            response = self.client.post(
                'v1/guests/',
                data=json.dumps(dict(guest = dict(first_name = "Tim", last_name="Hortons", organization = "TIMS", email="tim.hortons@tims.ca"))),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Guest creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['guest']['first_name'], 'Tim')
            self.assertTrue(data['guest']['last_name'], 'Hortons')
            self.assertTrue(data['guest']['organization'], 'TIMS')
            self.assertTrue(data['guest']['email'], 'tim.hortons@tims.ca')
            response = self.client.get(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['guest']['first_name'], 'Tim')
            self.assertTrue(data['guest']['last_name'], 'Hortons')
            self.assertTrue(data['guest']['organization'], 'TIMS')
            self.assertTrue(data['guest']['email'], 'tim.hortons@tims.ca')
            self.assertIsInstance(data['guest'], dict)
            self.assertTrue(response.content_type == 'application/json')

    def test_no_guest_returned_by_given_id(self):
        """
        Test there is no guest/no guest returned with given Id
        :return:
        """
        with self.client:
            token = self.get_user_token()

            response = self.client.get(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Guest not found')
            self.assertTrue(response.content_type == 'application/json')

    def test_deletion_handles_no_guest_found_by_id(self):
        """
        Show that a 404 response is returned when an un existing guest is being deleted.
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Guest resource cannot be found')
            self.assertTrue(response.content_type == 'application/json')

    def test_request_for_deleting_guest_has_integer_id(self):
        """
        Test that only integer guest Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/guests/dsfgsdsg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Guest Id')

    def test_guest_is_updated(self):
        """
        Test that the Guest details(name) is updated
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()

            # Create a Guest
            response = self.client.post(
                'v1/guests/',
                data=json.dumps(dict(guest = dict(first_name = "Tim", last_name="Hortons", organization = "TIMS", email="tim.hortons@tims.ca"))),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )

            # Test Guest creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['guest']['first_name'], 'Tim')
            self.assertTrue(data['guest']['last_name'], 'Hortons')
            self.assertTrue(data['guest']['organization'], 'TIMS')
            self.assertTrue(data['guest']['email'], 'tim.hortons@tims.ca')

            # Update the guest first name
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(first_name = "John"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['guest']['first_name'], 'John')
            self.assertEqual(data['guest']['guest_id'], 1)

            # Update the guest last_name
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(last_name = "Wick"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['guest']['last_name'], 'Wick')
            self.assertEqual(data['guest']['guest_id'], 1)

            # Update the guest organization
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(organization = "DSDC"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['guest']['organization'], 'DSDC')
            self.assertEqual(data['guest']['guest_id'], 1)

    def test_id_of_guest_to_be_edited_does_not_exist(self):
        """
        Test the guest to be updated does not exist.
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            # Update the guest name
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(first_name = "John"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 404)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'The Guest with Id 1 does not exist')

    def test_id_of_guest_to_be_edited_is_invalid(self):
        """
        Test the guest id is invalid.
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            # Update the guest name
            res = self.client.put(
                'v1/guests/guestid',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(first_name = "Tim", last_name="Hortons", organization = "TIMS", email="tim.hortons@tims.ca"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Guest Id')

    def test_content_type_for_editing_guest_is_json(self):
        """
        Test that the content type used for the request is application/json
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(first_name = "Tim", last_name="Hortons", organization = "TIMS", email="tim.hortons@tims.ca")))
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 202)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be json')

    def test_required_guest_name_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(name) exists and has value in the request payload
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(name = ""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_required_guest_location_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(location) exists and has value in the request payload
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(location=""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_required_guest_time_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(time) exists and has value in the request payload
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(guest = dict(time = ""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_guest_is_deleted(self):
        """
        Test that a Guest is deleted successfully
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            response = self.client.post(
                'v1/guests/',
                data=json.dumps(dict(guest = dict(first_name = "Tim", last_name="Hortons", organization = "TIMS", email="tim.hortons@tims.ca"))),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Guest creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['guest']['first_name'], 'Tim')
            self.assertTrue(data['guest']['last_name'], 'Hortons')
            self.assertTrue(data['guest']['organization'], 'TIMS')
            self.assertTrue(data['guest']['email'], 'tim.hortons@tims.ca')
            # Delete the created Guest
            res = self.client.delete(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Guest Deleted successfully')
            self.assertTrue(res.content_type == 'application/json')

    def test_400_bad_requests(self):
        """
        Test for Bad requests - 400s
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/guests/1',
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Bad Request')

    def test_guests_returned_when_searched(self):
        """
        Test Guests are returned when a query search q is present in the url
        Also test that the next page pagination string is 'http://localhost/guests/1/items/?page=2'
        and previous is none
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_guests(token)
            response = self.client.get(
                'v1/guests/?q=T',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['guests'], list, 'Items must be a list')
            self.assertEqual(len(data['guests']), 1)
            self.assertEqual(data['guests'][0]['guest_id'], 2)
            self.assertEqual(data['count'], 1)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], None)
            self.assertEqual(response.status_code, 200)

    def test_guests_returned_when_searched_2(self):
        """
        Test Guests are returned when a query search q is present in the url
        Also test that the next page pagination string is None
        and previous is 'http://localhost/guests/1/items/?page=1'
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_guests(token)
            response = self.client.get(
                'v1/guests/?q=T&page=2',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['guests'], list, 'Items must be a list')
            self.assertEqual(len(data['guests']), 0)
            self.assertEqual(data['count'], 0)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], 'http://localhost/v1/guests/?q=T&page=1')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
