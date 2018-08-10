from flask import Blueprint, jsonify, make_response, request

from app.models.user import User
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('user', __name__)


# @app.route('/user', methods=['GET'])
# @check_webtoken(extra_token=True)
# def get(token_data):
#     '''user_idに紐づくuser情報取得
#     Returns:
#         dict:
#             nick_name, profile, twitter_name
#     '''
#     try:
#         user_id = token_data.get('user_id')
#
#         result = User.get(user_id)
#
#         return jsonify(result)
#     except Exception as e:
#         return make_response('', 500)
#
#
# @app.route('/user/<user_id>', methods=['GET'])
# @check_webtoken
# def get_by_user_id(user_id):
#     '''user_idに紐づくuser情報取得
#     Returns:
#         dict:
#             nick_name, profile, twitter_name
#     '''
#     try:
#         result = User.get(user_id)
#
#         return jsonify(result)
#     except Exception as e:
#         return make_response('', 500)
#
#
# @app.route('/user', methods=['PUT'])
# @check_webtoken(extra_token=True)
# def put(token_data):
#     '''user情報(emailとpassword以外)を更新
#     Args:
#         dict:
#             nick_name, profile, twitter_name
#     Returns:
#         dict:
#             nick_name, profile, twitter_name
#     '''
#     try:
#         params = request.json
#
#         user_id = token_data.get('user_id')
#         data = {
#             'nick_name': params.get('nick_name'),
#             'profile': params.get('profile'),
#             'twitter_name': params.get('twitter_name'),
#         }
#
#         User.put(user_id, data)
#
#         result = User.get(user_id=user_id)
#
#         return make_response(jsonify(result), 200)
#     except Exception as e:
#         if str(e) == 'over length':
#             return make_response('', 400)
#
#         return make_response('', 500)
#
#
# @app.route('/user/password', methods=['PUT'])
# @check_webtoken(extra_token=True)
# def put_password(token_data):
#     '''userのpasswordを更新
#     Args:
#         dict:
#             password, new_password
#     Returns:
#         200:    正常更新
#         500:    サーバエラー
#     '''
#     try:
#         params = request.json
#
#         user_id = token_data.get('user_id')
#         password = params.get('password')
#         new_password = params.get('new_password')
#
#         User.put_password(user_id, password, new_password)
#
#         return make_response('', 200)
#     except Exception as e:
#         if str(e) == 'invalid password':
#             return make_response('', 400)
#
#         return make_response('', 500)
