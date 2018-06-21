'''WeConnect Reviews Test File'''
import unittest
import json
from V1 import app


class RequestsTestCase(unittest.TestCase):
    '''Reviews Class Tests'''

    def setUp(self):
        self.app = app.test_client(self)
        # User 1
        self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(dict(
                email="kelvin@live.com", username="kelvin",
                password="12345678")), content_type="application/json")
        self.login_user = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(dict(
                username="kelvin",
                password="12345678")), content_type="application/json")
        self.access_token = json.loads(
            self.login_user.data.decode())['access_token']

        # User 2
        self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(dict(
                email="lynn@live.com", username="lynn",
                password="12345678")), content_type="application/json")
        self.login_user2 = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(dict(
                username="lynn",
                password="12345678")), content_type="application/json")

        self.access_token2 = json.loads(
            self.login_user2.data.decode())['access_token']

        # Ride 1
        self.app.post(
            "/api/v1/rides",
            data=json.dumps(dict(
                category="SUV", pick_up="Uthiru",
                drop_off="CBD", date_time="20th June 12.00 A.M",
                price="Ksh. 700")),
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})

        self.dict = dict(
            category="Limousine", pick_up="Uthiru",
            drop_off="CBD", date_time="20th June 12.00 A.M",
            price="Ksh. 700")

    def test_add_request(self):
        '''test add review'''
        response = self.app.post(
            "/api/v1/rides/1/requests",
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 201)

    def test_get_requests(self):
        '''Test get all reviews'''
        response = self.app.get(
            "/api/v1/rides/1/requests",
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
