from flask import Blueprint, jsonify, make_response

from app.models.sort import Sort
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('sort', __name__)


@app.route('/sorts', methods=['GET'])
@check_webtoken
def get():
    '''すべてのsort取得
    Returns:
        200:
            list(dict):
                sort情報のリスト
        500: サーバエラー
    '''
    try:
        result = Sort.get_all()

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)
