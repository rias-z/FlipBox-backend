from flask import Blueprint, jsonify, make_response, request
from datetime import datetime, timezone, timedelta

from app.models.user import User
from app.models.good import Good
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('top', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


@app.route('/trend', methods=['GET'])
def get_trend():
    '''トレンドを表示
    Returns:
    '''
    try:
        users = User.all()
        user_flip_list = []
        for user in users:
            flips = Good.get_flips_by_user_id(user.get('user_id'))
            if len(flips) is 0:
                return make_response([], 200)
            item_cnt_cnt = 0
            bookmark_cnt_cnt = 0
            good_cnt_cnt = 0
            for flip in flips:
                item_cnt_cnt += int(flip.get('item_cnt'))
            for flip in flips:
                bookmark_cnt_cnt += int(flip.get('bookmark_cnt'))
            for flip in flips:
                good_cnt_cnt += int(flip.get('good_cnt'))
            user_flip = {
                'flips': flips,
                'author': user,
                'item_cnt': item_cnt_cnt,
                'bookmark_cnt': bookmark_cnt_cnt,
                'good_cnt': good_cnt_cnt,
                'create_at': flips[0].get('create_at')
            }
            user_flip_list.append(user_flip)

        result = sorted(user_flip_list, key=lambda x: x["good_cnt"],
                        reverse=True)
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/timeline', methods=['GET'])
def get_timeline():
    '''タイムラインを表示
    Returns:
    '''
    try:
        users = User.all()
        user_flip_list = []
        for user in users:
            flips = Good.get_flips_by_user_id(user.get('user_id'))
            if len(flips) is 0:
                return make_response([], 200)
            item_cnt_cnt = 0
            bookmark_cnt_cnt = 0
            good_cnt_cnt = 0
            for flip in flips:
                item_cnt_cnt += int(flip.get('item_cnt'))
            for flip in flips:
                bookmark_cnt_cnt += int(flip.get('bookmark_cnt'))
            for flip in flips:
                good_cnt_cnt += int(flip.get('good_cnt'))
            user_flip = {
                'flips': flips,
                'author': user,
                'item_cnt': item_cnt_cnt,
                'bookmark_cnt': bookmark_cnt_cnt,
                'good_cnt': good_cnt_cnt,
                'create_at': flips[0].get('create_at')
            }
            user_flip_list.append(user_flip)

        result = sorted(user_flip_list, key=lambda x: x["good_cnt"],
                        reverse=True)
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)
