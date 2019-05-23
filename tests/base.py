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
            'v1/events',
            data=json.dumps(dict(event = dict(name = "Some Event", location="7 Bayview yards", time = "2019-05-22 10:00:00", eval_link="http://google.ca"))),
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['status'], 'success')
        self.assertTrue(data['event']['event_name'], 'Some Event')
        self.assertTrue(data['event']['event_location'], '7 Bayview yards')
        self.assertTrue(data['event']['event_time'], '2019-05-22 10:00:00')
        self.assertTrue(data['event']['event_eval_link'], 'http://google.ca')
        self.assertIsInstance(data['event']['event_id'], int, msg='Value should be a string')


    def create_guest(self, token):
        """
        Helper function to create a guest
        :return:
        """
        response = self.client.post(
            'v1/guests',
            data=json.dumps(dict(guest = dict(first_name = "Tim", last_name="Hortons", organization = "TIMS", email="tim.hortons@tims.ca"))),
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['status'], 'success')
        self.assertTrue(data['guest']['first_name'], 'Tim')
        self.assertTrue(data['guest']['last_name'], 'Hortons')
        self.assertTrue(data['guest']['organization'], 'TIMS')
        self.assertTrue(data['guest']['email'], 'tim.hortons@tims.ca')
        self.assertIsInstance(data['guest']['guest_id'], int, msg='Value should be a string')

    def create_events(self, token):
        '''
        Helper function to create an event
        :return:
        '''
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
                'v1/events',
                data=json.dumps(dict(event)),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['event']['event_name'], event['event']['name'])
            self.assertTrue(data['event']['event_location'], event['event']['location'])
            self.assertTrue(data['event']['event_time'], event['event']['time'])
            try:
                self.assertTrue(data['event']['event_eval_link'], event['event']['eval_link'])
            except KeyError:
                pass
            self.assertIsInstance(data['event']['event_id'], int, msg='Value should be a string')


    def create_guests(self, token):
        '''
        Helper function to create a guest
        :return:
        '''
        guests = [
            {'guest': {'first_name' : 'John', 'last_name' : 'Wick', 'organization' : 'CDS', 'email' : 'email1@email.com'}},
            {'guest': {'first_name' : 'Bradd', 'last_name' : 'Pitt', 'organization' : 'CSE', 'email' : 'email2@email.com'}},
            {'guest': {'first_name' : 'Angelina', 'last_name' : 'Jolly', 'organization' : 'CBSA', 'email' : 'email3@email.com'}},
            {'guest': {'first_name' : 'Edna', 'last_name' : 'Mode', 'organization' : 'CRA', 'email' : 'email4@email.com'}},
            {'guest': {'first_name' : 'Randle', 'last_name' : 'McMurphy', 'organization' : 'CSPS', 'email' : 'email5@email.com'}},
            {'guest': {'first_name' : 'Optimus', 'last_name' : 'Prime', 'organization' : 'CFA', 'email' : 'email6@email.com'}},
            {'guest': {'first_name' : 'Niyongabo', 'last_name' : 'Jean', 'organization' : 'CFA', 'email' : 'email7@email.com'}}
        ]
        for guest in guests:
            response = self.client.post(
                'v1/guests',
                data=json.dumps(dict(guest)),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['guest']['first_name'], guest['guest']['first_name'])
            self.assertTrue(data['guest']['last_name'], guest['guest']['last_name'])
            self.assertTrue(data['guest']['organization'], guest['guest']['organization'])
            self.assertTrue(data['guest']['email'], guest['guest']['email'])