from flask import Blueprint, jsonify, make_response, request
from datetime import datetime, timezone, timedelta

from app.models.flip import Flip
from app.models.tag import Tag
from app.models.flip_tag import FlipTag
from app.models.user import User

app = Blueprint('search', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


@app.route('/search', methods=['GET'])
def get_flips():
    '''検索結果を表示
    Returns:
    '''
    try:
        query = request.args.get('q')
        flips = Flip.get_by_query(query)
        result = []
        for flip in flips:
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


@app.route('/tags/<tag_name>', methods=['GET'])
def get_tags(tag_name):
    '''タイムラインを表示
    Returns:
    '''
    try:
        tags_query = request.args.get('tags')
        if tags_query is None:
            '''
                queryがない時の挙動
            '''
            tag = Tag.get_by_tag_name(tag_name)
            flips = FlipTag.get_by_flips_by_tag_id(tag.get('tag_id'))
            result = []
            for flip in flips:
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
        else:
            '''
                tags=<tags>のqueryがある時の挙動
            '''
            tag_list = []
            for tag_query in tags_query:
                tag = Tag.get_by_tag_name(tag_query)
                tag_list.append(tag)

            flips_list = []
            for tag2 in tag_list:
                flips = FlipTag.get_by_flips_by_tag_id(tag2.get('tag_id'))
                flips_list.append(flips)

            if len(flips_list) is 0:
                return jsonify([])

            flips_list2 = sorted(set(flips_list), key=flips_list.index)
            result = []
            for f in flips_list2:
                tags = FlipTag.get_by_flip_id(f.get('flip_id'))
                tags_list = [tag.get('name') for tag in tags]
                tags_dict = {'tags': tags_list}
                user = User.get(f.get('user_id'))
                author_dict = {
                    'user_id': user.get('user_id'),
                    'username': user.get('username')
                }
                f.update(tags_dict)
                f.update(author_dict)
                result.append(f)
            return jsonify(result)
    except Exception as e:
        return make_response('', 500)

