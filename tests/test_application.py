from tests.base import BaseTestCase
import unittest
import json


class TestMainAppCase(BaseTestCase):
    def test_page_not_found(self):
        """
        Test that a given route does not exist in the application
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/home',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assert404(response)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Endpoint not found')


    def test_http_method_not_found(self):
        with self.client:
            response = self.client.delete(
                'v1/events/<event_id>/tickets',
                headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assert405(response)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'The method is not allowed for the requested URL')

    def test_docs_page(self):
        """
        Test that the homepage returns a 200 response status code
        :return:
        """
        with self.client:
            response = self.client.get('/docs/')
            self.assert200(response)


if __name__ == "__main__":
    unittest.main()