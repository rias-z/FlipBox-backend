from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, make_response, request

from app.models.comment import Comment
from app.models.user import User
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('comment', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


@app.route('/comment', methods=['POST'])
@check_webtoken(extra_token=True)
def post_comment(token_data):
    '''comment投稿
    Args:
    Returns:
    '''
    try:
        params = request.json

        user_id = token_data.get('user_id')
        flip_id = params.get('flip_id')

        params.update({
            'user_id': user_id,
            'create_at': datetime.now(JST)
        })

        Comment.post(params)
        comments = Comment.get_by_flip_id(flip_id)
        result = []
        for comment in comments:
            result_dict = {'comment': comment,
                           'user': User.get(comment.user_id)}
            result.append(result_dict)

        return jsonify(result)
    except Exception as e:
        if str(e) == 'over text length':
            result = {
                'error_message': 'テキストが長すぎます'
            }
            return make_response(jsonify(result), 400)

        return make_response('', 500)


@app.route('/comment', methods=['PUR'])
@check_webtoken(extra_token=True)
def put_comment(token_data):
    '''comment投稿
    Args:
    Returns:
    '''
    try:
        params = request.json
        comment_id = params.get('comment_id')

        Comment.put(params)
        result = Comment.get(comment_id)

        return jsonify(result)
    except Exception as e:
        if str(e) == 'over text length':
            result = {
                'error_message': 'テキストが長すぎます'
            }
            return make_response(jsonify(result), 400)

        return make_response('', 500)
