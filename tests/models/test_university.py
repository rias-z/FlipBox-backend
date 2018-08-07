import unittest

from app.models.university import University
from tests.base import AbstractTest


class UniversityTest(AbstractTest):
    tables = ['university']

    def test_get_all(self):
        '''すべてのuniversity情報取得'''
        self.load_fixtures()

        university = University()

        actual = university.all()
        expect = [
            {'university_id': 1, 'name': 'test1', 'domain': 'test1.ac.jp'},
            {'university_id': 2, 'name': 'test2', 'domain': 'test2.ac.jp'},
        ]

        self.assertListEqual(expect, actual)

    def test_get(self):
        '''university_idに紐づくuniversity情報取得'''
        self.load_fixtures()

        university = University()

        actual = university.get(1)
        expect = {
            'university_id': 1, 'name': 'test1', 'domain': 'test1.ac.jp'
        }

        self.assertDictEqual(expect, actual)

    def test_get_no_university(self):
        '''university_idに紐づくuniversity情報が存在しない場合'''
        self.load_fixtures()

        university = University()

        actual = university.get(100)

        self.assertEqual(None, actual)


if __name__ == '__main__':
    unittest.main()
