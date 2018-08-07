import os
import sys
from unittest import TestLoader, TextTestRunner

from app.config import init_config
from tests.utils import drop_database


def run():
    init_config(env='test')

    # テスト用データベースの削除
    drop_database()

    loader = TestLoader()

    base_dir = os.path.dirname(__file__)
    package = loader.discover(base_dir)

    runner = TextTestRunner(verbosity=2)

    result = runner.run(package)

    if len(result.errors) > 0 or len(result.failures) > 0:
        sys.exit(3)
