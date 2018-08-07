from flask import Blueprint, jsonify, make_response

from app.models.category import Category
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('category', __name__)


@app.route('/category', methods=['GET'])
@check_webtoken
def get():
    '''すべてのcategory取得
    Returns:
        200:
            list(dict):
                category情報のリスト
        500: サーバエラー
    '''
    try:
        result = Category.get()

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)
