import json
from datetime import datetime
import unittest

from app import init_server
from app.models.user import User
from app.views.utils.auth import generate_token
from tests.base import AbstractTest


class ThreadAPITest(AbstractTest):
    tables = ['user', 'category', 'thread']
    test_tables = ['user', 'category', 'thread']

    client = init_server().test_client()

    def setUp(self):
        super(ThreadAPITest, self).setUp()

        self.load_fixtures()

        user = User.get_user_secret(user_id=1)
        token = generate_token(
            user_id=user.get('user_id'), email=user.get('email')
        )
        self.headers = {'Authorization': 'Bearer %s' % token}

    # TODO テストにおけるdatetimeの扱いをどうにかする #2
    def test_get_all_by_c_id(self):
        '''GET /threads 200 OK
        '''
        data = {
            'category_id': 1,
            'sort_id': 1,
            'paging': 1,
        }

        response = self.client.get(
            '/threads',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers
        )

        self.assertEqual(200, response.status_code)

    def test_get_thread(self):
        '''GET /thread 200 OK
        '''
        thread_id = 1

        response = self.client.get(
            '/thread/%d' % thread_id,
            headers=self.headers
        )

        actual = json.loads(response.data.decode())
        actual.get('thread').update({
            'create_at': datetime.strptime(
                actual.get('thread').get('create_at'),
                "%a, %d %b %Y %H:%M:%S GMT"
            ),
            'update_at': datetime.strptime(
                actual.get('thread').get('update_at'),
                "%a, %d %b %Y %H:%M:%S GMT"
            ),
        })

        thread = self.filter_test_data(
            table='thread', field='thread_id', target=1
        )[0]
        expect = {
            'thread': thread,
            'comments': []
        }

        self.assertDictEqual(expect, actual)

    # TODO テストにおけるdatetimeの扱いをどうにかする #2
    def test_post(self):
        '''POST /thread 200 OK
        '''
        data = {
            'title': 'title24',
            'category_id': 1,
            'comment_text': 'hello',
        }

        response = self.client.post(
            '/thread',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers
        )

        self.assertEqual(200, response.status_code)

    def test_delete_thread(self):
        '''DELETE /thread 200 OK
        '''
        thread_id = 1

        response = self.client.delete(
            '/thread/%d' % thread_id,
            headers=self.headers
        )

        self.assertEqual(200, response.status_code)

        response = self.client.get(
            '/thread/%d' % thread_id,
            headers=self.headers
        )

        self.assertEqual(400, response.status_code)

    def test_delete_no_thread(self):
        '''DELETE /thread 400 NOT FOUND
        '''
        thread_id = 100

        response = self.client.delete(
            '/thread/%d' % thread_id,
            headers=self.headers
        )

        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
