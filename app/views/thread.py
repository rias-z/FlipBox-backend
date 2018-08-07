from flask import Blueprint, jsonify, make_response, request

from app.models.comment import Comment
from app.models.thread import Thread
from app.models.user import User
from app.views.utils import parse_params
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('thread', __name__)


@app.route('/threads', methods=['GET'])
@check_webtoken
def get_all_by_c_id():
    '''category_idに紐づけられたthreadリストの取得
    Args:
        QueryString:
            category_id:    カテゴリID
            sort_id:        ソートID
            paging:         ページング番号
    Returns:
        200:
            list(dict):
                threads情報(dict)のリスト
        400: パラメータ不正
        500: サーバエラー

    ページング番号 1の時は1~10，2の時11~20のthreadを取得
    '''
    try:
        params = parse_params(request.args)

        category_id = int(params.get('category_id'))
        sort_id = int(params.get('sort_id'))
        paging = int(params.get('paging'))

        if not category_id or not sort_id or not paging:
            return make_response('', 400)

        result = Thread.get_all_by_c_id(
            category_id,
            sort_id,
            paging
        )

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/threads/<title>', methods=['GET'])
@check_webtoken
def get_by_title(title):
    '''titleからthread情報取得
    Args:
        200:
            list(dict):
                threads情報(dict)のリスト
        400: パラメータ不正
        500: サーバエラー
    '''
    try:
        result = Thread.get_by_title(title=title)

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/thread/<thread_id>', methods=['GET'])
@check_webtoken
def get(thread_id):
    '''thread_idからthread情報取得
    Args:
        thread_id:  スレッドID
    Returns:
        200:
            dict:
                thread: thread情報
                comments: list(dict) comment情報のリスト
        400: threadが存在しない場合
        500: サーバエラnー
    '''
    try:
        result = Thread.get(thread_id)

        if not result:
            return make_response('', 400)

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/thread', methods=['POST'])
@check_webtoken(extra_token=True)
def post(token_data):
    '''threadを作成
    Args:
        title:          スレッドタイトル
        category_id:    カテゴリID
        comment_text:        1コメ
    Returns:
        dict:
            作成されたthread情報
    '''
    try:
        params = request.json

        new_thread = Thread.post(
            title=params.get('title'),
            category_id=params.get('category_id')
        )

        user_id = token_data.get('user_id')

        user = User.get(user_id)

        data = {
            'name': user.get('nick_name'),
            'thread_id': new_thread.get('thread_id'),
            'text': params.get('comment_text'),
            'user_id': user_id,
        }

        Comment.post(data)

        result = Thread.get(new_thread.get('thread_id'))

        return jsonify(result)
    except Exception as e:
        if str(e) == 'over title length':
            result = {
                'error_message': 'タイトルが長すぎます'
            }
            return make_response(jsonify(result), 400)

        return make_response('', 500)


@app.route('/thread/<thread_id>', methods=['DELETE'])
@check_webtoken
def delete(thread_id):
    '''threadを削除
    同時に，thread_idに紐づくcommentテーブルも削除する
    Args:
        thread_id:  スレッドID
    Returns:
        200:    正常削除
        400:    threadが存在しない
        500:    サーバエラー
    '''
    try:
        Thread.delete(thread_id)

        return make_response('', 200)
    except Exception as e:
        if str(e) == 'thread not found':
            return make_response('', 400)

        return make_response('', 500)
