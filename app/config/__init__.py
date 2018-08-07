import copy
import os
import yaml

from utils import get_in


class ConfigStatus:
    _config = None
    _config_dir = os.path.dirname(__file__)

    @classmethod
    def init(cls, env='develop'):
        _config = {}

        # 初期設定
        _config.update(cls._load(cls._get_path('config.yaml')))

        for path in os.listdir(cls._config_dir):
            if path == 'env':
                conf_path = '%s/%s/%s.yaml' % (cls._config_dir, path, env)

                _config.update(cls._load(conf_path))
            else:
                if path.endswith('.yaml'):
                    _config.update(cls._load(cls._get_path(path)))

        cls._config = _config

    @classmethod
    def _load(cls, path):
        if not os.path.exists(path):
            raise Exception('Error: config file not found %s' % path)

        with open(path, 'r', encoding='utf-8') as f:
            conf = yaml.load(f)
            return conf if conf else {}

    @classmethod
    def _get_path(cls, filename):
        return ('%s/%s') % (cls._config_dir, filename)

    @classmethod
    def get_config(cls, *params):
        '''
        ex:
            get_config('develop', 'server')
        '''
        if cls._config is None:
            raise Exception('Error: get_config() execute initialized config')

        _config = get_in(cls._config, *params)

        return copy.deepcopy(_config)


def init_config(env='develop'):
    ConfigStatus.init(env=env)


def current_config(*params):
    return ConfigStatus.get_config(*params)


def create_dburl():
    conf_db = current_config('db')

    dburl = current_config('dburl').format(
        user=conf_db.get('user'),
        passwd=conf_db.get('passwd'),
        host=conf_db.get('host'),
        port=conf_db.get('port'),
        db=conf_db.get('db'),
        charset=conf_db.get('charset'),
    )

    return dburl
