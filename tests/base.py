from app import app, db
from flask_testing import TestCase
import json


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        """
        Create the database
        :return:
        """
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """
        Drop the database tables and also remove the session
        :return:
        """
        db.session.remove()
        db.drop_all()

    def register_user(self, email, password):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            'v1/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))

    def get_user_token(self):
        """
        Get a user token
        :return:
        """
        auth_res = self.register_user('example@gmail.com', '123456')
        return json.loads(auth_res.data.decode())['auth_token']

    def create_event(self, token):
        """
        Helper function to create an event
        :return:
        """
        response = self.client.post(
            'v1/events/',
            data=json.dumps(dict(event = dict(name = "Some Event", location="7 Bayview yards", time = "2019-05-22 10:00:00", eval_link="http://google.ca"))),
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['status'], 'success')
        self.assertTrue(data['event']['name'], 'Some Event')
        self.assertTrue(data['event']['location'], '7 Bayview yards')
        self.assertTrue(data['event']['time'], '2019-05-22 10:00:00')
        self.assertTrue(data['event']['eval_link'], 'http://google.ca')
        self.assertIsInstance(data['event_id'], int, msg='Value should be a string')



        def create_events(self, token):
        """
        Helper function to create an event
        :return:
        """
        events = [
            {'event': {'name' : 'Public Service Orientation Workshop', 'location' : 'Ottawa', 'time' : '2019-05-22 15:00:00'}},
            {'event': {'name' : 'Administrative Professionals Forum', 'location' : '1781 Russell Road, Ottawa, ON, K1G 0N1', 'time' : '2019-05-23 15:00:00', 'eval_link' : 'http://youtube.com'}},
            {'event': {'name' : 'Welcoming Event for Students', 'location' : 'Montreal', 'time' : '2019-05-23 15:00:00'}},
            {'event': {'name' : 'HR-to-Pay Engagement Day', 'location' : 'Toronto', 'time' : '2019-05-23 15:00:00', 'eval_link' : 'http://facebook.com'}},
            {'event': {'name' : 'Rebuilding Public Trust: The New Impact Assessment Regime', 'location' : 'Halifax', 'time' : '2019-08-23 09:00:00'}},
            {'event': {'name' : 'Innovating to Support Official Languages', 'location' : 'Sudbury', 'time' : '2019-03-17 11:00:00', 'eval_link' : 'http://web.whatsapp.com'}}
        ]
        for event in events:
            response = self.client.post(
                'v1/events/',
                data=json.dumps(dict(event)),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['name'], event['name'])
            self.assertTrue(data['event']['location'], event['location'])
            self.assertTrue(data['event']['time'], event['time'])
            if(event['eval_link'] is not None):
                self.assertTrue(data['event']['eval_link'], event['eval_link'])
            self.assertIsInstance(data['event_id'], int, msg='Value should be a string')