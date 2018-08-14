from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, make_response, request

from app.models.bookmark import Bookmark
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('bookmark', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


@app.route('/bookmark', methods=['POST'])
@check_webtoken(extra_token=True)
def post(token_data):
    try:
        user_id = token_data.get('user_id')
        flip_id = request.data.flip_id
        params = {'user_id': user_id, 'flip_id': flip_id,
                  'order_id': 1, 'create_at': datetime.now(JST)}
        bookmark = Bookmark.post(params)
        result = {'flip_id': bookmark.flip_id}
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/bookmark/<bookmark_id>', methods=['DELETE'])
@check_webtoken(extra_token=True)
def delete(bookmark_id):
    Bookmark.delete(bookmark_id)
