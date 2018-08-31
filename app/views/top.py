from flask import Blueprint, jsonify, make_response, request
from datetime import datetime, timezone, timedelta

from app.models.flip import Flip
from app.models.flip_tag import FlipTag
from app.models.user import User
from app.models.follow import Follow
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('top', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


@app.route('/trend', methods=['GET'])
def get_trend():
    '''トレンドを表示
    Returns:
    '''
    try:
        flips = Flip.get_order_by()
        for flip in flips:
            count = int(flip.get('bookmark_cnt')) + int(flip.get('good_cnt'))
            flip['count'] = count
        new_flips = sorted(flips, key=lambda x: x["count"], reverse=True)
        result = []
        for flip in new_flips:
            tags = FlipTag.get_by_flip_id(flip.get('flip_id'))
            tags_list = [tag.get('name') for tag in tags]
            tags_dict = {'tags': tags_list}
            user = User.get(flip.get('user_id'))
            author_dict = {
                'user_id': user.get('user_id'),
                'username': user.get('username')
            }
            flip.update(tags_dict)
            flip.update(author_dict)
            result.append(flip)
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/timeline', methods=['GET'])
@check_webtoken(extra_token=True)
def get_timeline(token_data):
    '''タイムラインを表示
    Returns:
    '''
    try:
        follows = Follow.get_to_follow_users(token_data.get('user_id'))
        users_list = []
        for follow in follows:
            users = Follow.get_from_follow_users(follow.get('user_id'))
            users_list.append(users)

        flips_list = []
        for user in users_list:
            flips = Flip.get_by_user_id(user.get('user_id'))
            flips_list.extend(flips)

        result = []
        for flip in flips_list:
            tags = FlipTag.get_by_flip_id(flip.get('flip_id'))
            tags_list = [tag.get('name') for tag in tags]
            tags_dict = {'tags': tags_list}
            user = User.get(flip.get('user_id'))
            author_dict = {
                'user_id': user.get('user_id'),
                'username': user.get('username')
            }
            flip.update(tags_dict)
            flip.update(author_dict)
            result.append(flip)
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)
