import json
import unittest

from app import init_server
from app.models.user import User
from app.views.utils.auth import generate_token
from tests.base import AbstractTest


class CommentAPITest(AbstractTest):
    tables = ['user', 'category', 'thread', 'comment']
    test_tables = ['user', 'category', 'thread', 'comment']

    client = init_server().test_client()

    def setUp(self):
        super(CommentAPITest, self).setUp()

        self.load_fixtures()

        user = User.get_user_secret(user_id=1)
        token = generate_token(
            user_id=user.get('user_id'), email=user.get('email')
        )
        self.headers = {'Authorization': 'Bearer %s' % token}

    # TODO テストにおけるdatetimeの扱いをどうにかする #2
    def test_post_comment(self):
        '''POST /comment 201 CREATE
        '''
        data = {
            'thread_id': 1,
            'text': 'particle',
        }

        response = self.client.post(
            '/comment',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers
        )

        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
