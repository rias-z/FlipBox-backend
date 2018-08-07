import unittest

from app.models.item import Item
from tests.base import AbstractTest


class ItemTest(AbstractTest):
    tables = ['item']

    def test_get(self):
        self.load_fixtures()

        item = Item()

        actual = item.get()
        expect = [
            {'item_id': 1, 'name': '雑談'},
            {'item_id': 2, 'name': '恋愛'},
            {'item_id': 3, 'name': '学業'},
        ]

        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
