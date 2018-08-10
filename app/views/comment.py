from flask import Blueprint, jsonify, make_response, request

from app.models.comment import Comment
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('comment', __name__)


# @app.route('/comment', methods=['POST'])
# @check_webtoken(extra_token=True)
# def post_comment(token_data):
#     '''comment投稿
#     Args:
#         text:       コメントテキスト
#         thread_id:  スレッドID
#     Returns:
#         200:    正常終了
#             list(dict):
#                 comment情報のリスト
#         500:    サーバエラー
#     '''
#     try:
#         params = request.json
#
#         user_id = token_data.get('user_id')
#         user = User.get(user_id=user_id)
#
#         params.update({
#             'user_id': user_id,
#             'name': user.get('nick_name')
#         })
#
#         result = []
#
#         return make_response(jsonify(result), 201)
#     except Exception as e:
#         if str(e) == 'over text length':
#             result = {
#                 'error_message': 'テキストが長すぎます'
#             }
#             return make_response(jsonify(result), 400)
#
#         return make_response('', 500)
