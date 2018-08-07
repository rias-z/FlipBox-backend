from flask import Flask
from flask_cors import CORS

from app.views import get_blueprints
from app.config import current_config


def init_server():
    server = Flask(__name__)
    CORS(server)

    # blueprintの設定
    blueprints = get_blueprints()
    for blueprint in blueprints:
        server.register_blueprint(blueprint)

    return server


def run(env):
    server = init_server()

    config = current_config('server')

    server.run(
        host=config.get('host'),
        port=config.get('port'),
        debug=config.get('debug')
    )
