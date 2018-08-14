from flask import Blueprint, jsonify, make_response, request

from app.models.good import Good
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('good', __name__)


@app.route('/good', methods=['POST'])
@check_webtoken(extra_token=True)
def post(token_data):
    try:
        user_id = token_data.get('user_id')
        flip_id = request.data.flip_id
        params = {'user_id': user_id, 'flip_id': flip_id}
        good = Good.post(params)
        result = {'flip_id': good.flip_id}
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/good/<good_id>', methods=['DELETE'])
@check_webtoken(extra_token=True)
def delete(good_id):
    Good.delete(good_id)
