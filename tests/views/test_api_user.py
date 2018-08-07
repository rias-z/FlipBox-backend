import json
import unittest

from app import init_server
from app.models.user import User
from app.views.utils.auth import generate_token
from tests.base import AbstractTest


class UserAPITest(AbstractTest):
    tables = ['user']
    test_tables = ['user']

    client = init_server().test_client()

    def setUp(self):
        super(UserAPITest, self).setUp()

        self.load_fixtures()

        user = User.get_user_secret(user_id=1)
        token = generate_token(
            user_id=user.get('user_id'), email=user.get('email')
        )
        self.headers = {'Authorization': 'Bearer %s' % token}

    def test_get_user(self):
        '''GET /user 200 OK
        '''
        response = self.client.get(
            '/user',
            headers=self.headers
        )

        user = self.filter_test_data(
            table='user', field='user_id', target=1
        )[0]

        actual = json.loads(response.data.decode())
        expect = {
            'nick_name': user.get('nick_name'),
            'profile': user.get('profile'),
            'twitter_name': user.get('twitter_name'),
        }

        self.assertEqual(expect, actual)

    def test_put(self):
        '''PUT /user 200 OK
        '''
        data = {
            'nick_name': 'kiku',
            'profile': None,
            'twitter_name': 'matsu',
        }

        response = self.client.put(
            '/user',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers
        )

        self.assertEqual(200, response.status_code)

        response = self.client.get(
            '/user',
            headers=self.headers
        )

        actual = json.loads(response.data.decode())
        expect = data

        self.assertDictEqual(expect, actual)

    def test_put_password(self):
        '''PUT /user/password 200 OK
        '''
        new_password = 'test_new_pass1'

        user = self.filter_test_data(
            table='user', field='user_id', target=1
        )[0]

        data = {
            'password': user.get('password'),
            'new_password': new_password,
        }

        response = self.client.put(
            '/user/password',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers
        )

        self.assertEqual(200, response.status_code)

        actual = User.get_user_secret(1)
        expect = user
        expect.update({
            'password': new_password
        })

        self.assertDictEqual(expect, actual)

    def test_put_password_400(self):
        '''PUT /user/password 400 invalid password
        '''
        new_password = 'test_new_pass1'

        data = {
            'password': 'fake_password',
            'new_password': new_password,
        }

        response = self.client.put(
            '/user/password',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers
        )

        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
