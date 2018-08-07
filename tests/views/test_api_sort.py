import json
import unittest

from app import init_server
from app.models.user import User
from app.views.utils.auth import generate_token
from tests.base import AbstractTest


class SortAPITest(AbstractTest):
    tables = ['user', 'sort']
    test_tables = ['user', 'sort']

    client = init_server().test_client()

    def setUp(self):
        super(SortAPITest, self).setUp()

        self.load_fixtures()

        user = User.get_user_secret(user_id=1)
        token = generate_token(
            user_id=user.get('user_id'), email=user.get('email')
        )
        self.headers = {'Authorization': 'Bearer %s' % token}

    def test_get(self):
        '''GET /sorts 200 OK
        '''
        response = self.client.get(
            '/sorts',
            headers=self.headers
        )

        actual = json.loads(response.data.decode())
        expect = self.test_data.get('sort')

        self.assertListEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
