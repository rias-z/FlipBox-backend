import unittest

from tests.utils import (
    drop_tables,
    create_database,
    create_tables,
    drop_database,
    load_fixtures,
    load_test_data,
)


fixture_data_root = 'tests/resources/data'


class AbstractTest(unittest.TestCase):
    # 外部キー制約による読み込み順番に注意
    tables = []

    test_data = {}
    test_tables = []

    @classmethod
    def setUpClass(cls):
        # データベースの作成
        cls.create_database()

        # テーブルの作成
        cls.create_tables()

        # テストデータの読み込み
        cls.load_test_data()

    @classmethod
    def tearDownClass(cls):
        # データベースの削除
        cls.drop_database()

    def tearDown(self):
        self.drop_tables()

    @classmethod
    def create_database(cls):
        '''テスト用データベース作成
        '''
        create_database()

    @classmethod
    def drop_database(cls):
        '''テスト用データベース削除
        '''
        drop_database()

    @classmethod
    def create_tables(cls):
        '''テスト用テーブル作成
        '''
        create_tables()

    @classmethod
    def drop_tables(cls):
        '''テスト用テーブル削除
        '''
        drop_tables()

    @classmethod
    def load_fixtures(cls):
        '''テストデータ読み込み
        '''
        load_fixtures(fixture_data_root, cls.tables)

    @classmethod
    def load_test_data(cls):
        cls.test_data = load_test_data(fixture_data_root, cls.test_tables)

    @classmethod
    def get_test_data(cls, table):
        return cls.test_data.get(table)

    @classmethod
    def filter_test_data(
        cls, table, field=None, target=None, paging=None, reverse=False
    ):
        test_data = cls.test_data.get(table)

        if field and target:
            if type(target) is int:
                test_data = [r for r in test_data if r.get(field) == target]
            elif type(target) is list:
                test_data = [
                    r for t in target for r in test_data if r.get(field) == t
                ]
            else:
                raise Exception('invalid test_data target type')

        if reverse:
            test_data = list(reversed(test_data))

        if paging:
            offset = (paging - 1) * 10
            limit = paging * 10

            test_data = test_data[offset:limit]

        return test_data
