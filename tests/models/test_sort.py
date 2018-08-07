import unittest

from app.models.sort import Sort
from tests.base import AbstractTest


class SortTest(AbstractTest):
    tables = ['sort']

    def test_get_all(self):
        self.load_fixtures()

        sort = Sort()

        actual = sort.get_all()
        expect = [
            {'sort_id': 1, 'name': 'ID昇順'},
            {'sort_id': 2, 'name': 'ID降順'},
            {'sort_id': 3, 'name': '人気高い順'},
            {'sort_id': 4, 'name': '人気低い順'},
            {'sort_id': 5, 'name': 'コメント数多い順'},
            {'sort_id': 6, 'name': 'コメント数少ない順'},
        ]

        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
