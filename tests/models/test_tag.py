import unittest

from app.models.tag import Tag
from tests.base import AbstractTest


class TagTest(AbstractTest):
    tables = ['tag']

    def test_get_all(self):
        self.load_fixtures()

        tag = Tag()

        actual = tag.get_all()
        expect = [
            {'tag_id': 1, 'name': 'ID昇順'},
        ]

        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
