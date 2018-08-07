import json
import unittest

from app import init_server
from app.models.user import User
from app.views.utils.auth import generate_token
from tests.base import AbstractTest


class CategoryAPITest(AbstractTest):
    tables = ['user', 'category']

    client = init_server().test_client()

    def setUp(self):
        super().setUp()

        self.load_fixtures()

    def test_get(self):
        '''GET /category 200 OK
        '''
        user_id = 1

        email = User.get_email(user_id=user_id)
        token = generate_token(
            user_id=user_id, email=email
        )

        response = self.client.get(
            '/category',
            headers={'Authorization': 'Bearer %s' % token},
        )

        actual = json.loads(response.data.decode())
        expect = [
            {'category_id': 1, 'name': '雑談'},
            {'category_id': 2, 'name': '恋愛'},
            {'category_id': 3, 'name': '学業'},
        ]

        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
