from flask import Blueprint, jsonify, make_response

from app.models.university import University
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('university', __name__)


@app.route('/university', methods=['GET'])
@check_webtoken
def get_all():
    '''すべてのuniversity情報取得
    Returns:
        200:
            list(dict):
                university情報(dict)のリスト
        500: サーバエラー
    '''
    try:
        result = University.all()

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/university/<university_id>', methods=['GET'])
@check_webtoken
def get(university_id):
    '''university_idに紐づくuniversity情報取得
    Args:
        university_id:  大学ID
    Returns:
        200:
            list(dict):
                university情報(dict)のリスト
        500: サーバエラー
    '''
    try:
        result = University.get(university_id)

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)
