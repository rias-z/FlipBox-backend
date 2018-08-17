import unittest

from app.models.item import Item
from tests.base import AbstractTest


class ItemTest(AbstractTest):
    tables = ['item']

    def test_get(self):
        '''Item取得
        '''
        self.load_fixtures()

        item = Item()

        actual = item.get(1534547970293028)
        expect = {
            'item_id': 1534547970293028,
            'url': 'https://www.google.com/',
            'name': 'テストアイテム1',
            'description': 'テストのアイテム',
        }

        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
