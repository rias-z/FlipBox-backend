import json
import unittest

from app import init_server
from app.models.user import User
from app.models.provisional_user import ProvisionalUser
from tests.base import AbstractTest


class AuthAPITest(AbstractTest):
    tables = ['user']
    test_tables = ['user']

    client = init_server().test_client()

    def setUp(self):
        super(AuthAPITest, self).setUp()

        self.load_fixtures()

    def test_login(self):
        '''GET /login 200 OK
        '''
        user = self.filter_test_data(
            table='user', field='user_id', target=1
        )[0]

        data = {
            'email': user.get('email'),
            'password': user.get('password'),
        }

        response = self.client.get(
            '/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(200, response.status_code)

        # response.dataにweb_tokenがあるかチェック
        actual = json.loads(response.data.decode())
        exist_web_token = True if actual.get('web_token') else False

        self.assertEqual(True, exist_web_token)

    def test_login_failed(self):
        '''GET /login 400 FAILED LOGIN
        '''
        user = self.filter_test_data(
            table='user', field='user_id', target=1
        )[0]

        data = {
            'email': user.get('email'),
            'password': 'fake_password',
        }

        response = self.client.get(
            '/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(400, response.status_code)

    def test_register(self):
        '''POST /register 201 CREATE

        /auth/prog_userからlogin_tokenを擬似的に取得する
        '''
        email = 'iris@test_gmail.com'

        # login_tokenを擬似的に取得
        login_token = ProvisionalUser.post(email=email)

        data = {
            'email': email,
            'login_token': login_token,
            'password': 'password_iris',
            'nick_name': 'iris',
        }

        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(201, response.status_code)

        actual = User.get_by_email(email=email)
        expect = {
            'nick_name': 'iris',
            'profile': None,
            'twitter_name': None,
        }

        self.assertDictEqual(expect, actual)

    def test_register_error_duplicate_email(self):
        '''POST /register 400

        既に登録してあるemailの場合
        '''
        email = 'iris@test_gmail.com'

        # login_tokenを擬似的に取得
        login_token = ProvisionalUser.post(email=email)

        data = {
            'email': email,
            'login_token': login_token,
            'password': 'password_iris',
            'nick_name': 'iris',
        }

        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(201, response.status_code)

        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(400, response.status_code)

    def test_register_error_duplicate_nick_name(self):
        '''POST /register 400

        既に登録してあるemailの場合
        '''
        email = 'iris@test_gmail.com'

        # login_tokenを擬似的に取得
        login_token = ProvisionalUser.post(email=email)

        data = {
            'email': email,
            'login_token': login_token,
            'password': 'password_iris',
            'nick_name': 'iris',
        }

        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(201, response.status_code)

        # nick_name重複登録
        email = 'iris2@test_gmail.com'

        # login_tokenを擬似的に取得
        login_token = ProvisionalUser.post(email=email)

        data = {
            'email': email,
            'login_token': login_token,
            'password': 'password_iris',
            'nick_name': 'iris',
        }

        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
