from flask_testing import TestCase
from app import app
from flask import current_app
import unittest
import os


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        """
        Create an app with the development configuration
        :return:
        """
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_in_development(self):
        """
        Test that the development configs are set correctly.
        :return:
        """
        self.assertFalse(app.config['SECRET_KEY'] is 'false key')
        self.assertTrue(app.config['DEBUG'], True)
        self.assertTrue(app.config['BCRYPT_HASH_PREFIX'] == 4)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL',
                                                                           "postgresql://postgres:password@localhost/eplannerapi"))
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRY_DAYS'], 1)
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRY_SECONDS'], 20)
        self.assertEqual(app.config['EVENTS_AND_TICKETS_PER_PAGE'], 4)


class TestTestingConfig(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_in_testing(self):
        """
        Test that the testing configs are set correctly
        :return:
        """
        self.assertFalse(app.config['SECRET_KEY'] is 'false key')
        self.assertTrue(app.config['DEBUG'], True)
        self.assertTrue(app.config['TESTING'] is True)
        self.assertTrue(app.config['BCRYPT_HASH_PREFIX'] == 4)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL_TEST',
                                                                           "postgresql://postgres:password@localhost/eplannerapi_test"))
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRY_DAYS'], 0)
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRY_SECONDS'], 3)
        self.assertEqual(app.config['AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS'], 5)
        self.assertEqual(app.config['EVENTS_AND_TICKETS_PER_PAGE'], 4)


if __name__ == '__main__':
    unittest.main()
