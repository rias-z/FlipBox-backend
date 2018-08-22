from flask import Blueprint, jsonify, make_response, request
from datetime import datetime, timezone, timedelta

from app.models.flip import Flip
from app.models.flip_item import FlipItem
from app.models.flip_tag import FlipTag
from app.models.item import Item
from app.models.tag import Tag
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('flip', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


@app.route('/flip/<flip_id>', methods=['GET'])
def get_if_no_login(flip_id):
    '''flip_idに紐づくflip情報取得
    Returns:
    '''
    try:
        flip = Flip.get(flip_id)
        items = FlipItem.get_by_flip_id(flip_id)
        tags = FlipTag.get_by_flip_id(flip_id)

        result = {'flip': flip, 'items': items, 'tags': tags}

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


# TODO
# ログインされた場合のauthorを付加するバージョンを考える
# check_webTokenをつけた場合とつけてない場合で考えなくてはいけない


@app.route('/flip', methods=['POST'])
@check_webtoken(extra_token=True)
def post(token_data):
    try:
        params = request.json

        user_id = token_data.get('user_id')
        flip_id = str(datetime.now().timestamp()).replace('.', '')
        p_flip = params.get('flip')
        p_tags = p_flip.pop('tags')
        p_items = params.get('items')
        items_cnt = len(p_items)
        p_flip_items = []
        p_flip_tags = []

        for p_item in p_items:
            p_item['item_id'] = str(datetime.now().timestamp()).replace('.', '')
            item = Item.post(p_item)
            p_flip_item = {'flip_id': flip_id, 'item_id': item.get('item_id')}
            p_flip_items.append(p_flip_item)
        for tag_name in p_tags:
            p_tag = {'name': tag_name, 'tag_cnt': 1}
            tag = Tag.post(p_tag)
            p_flip_tag = {'flip_id': flip_id, 'tag_id': tag.get('tag_id')}
            p_flip_tags.append(p_flip_tag)

        p_flip['flip_id'] = flip_id
        p_flip['bookmark_cnt'] = 0
        p_flip['user_id'] = user_id
        p_flip['item_cnt'] = items_cnt
        p_flip['good_cnt'] = 0
        p_flip['create_at'] = datetime.now(JST)
        flip = Flip.post(p_flip)

        for p_fi in p_flip_items:
            FlipItem.post(p_fi)

        for p_ft in p_flip_tags:
            FlipTag.post(p_ft)

        result = {'flip_id': flip.get('flip_id')}
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/flip', methods=['PUT'])
@check_webtoken(extra_token=True)
def put(token_data):
    try:
        params = request.json
        user_id = token_data.get('user_id')
        if user_id is not params.get('user_id'):
            make_response('不正なユーザ', 400)

        p_flip = params.get('flip')
        flip_id = p_flip.get('flip_id')
        p_items = params.get('items')
        items_cnt = len(p_items)

        items = FlipItem.get_by_flip_id(flip_id)

        for item in items:
            Item.delete(item.get('item_id'))

        p_flip['flip_id'] = flip_id
        p_flip['bookmark_cnt'] = 0
        p_flip['user_id'] = user_id
        p_flip['item_cnt'] = items_cnt
        p_flip['good_cnt'] = 0
        p_flip['create_at'] = datetime.now(JST)
        flip = Flip.post(p_flip)

        result = {'flip_id': flip.get('flip_id')}
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/flip/<flip_id>', methods=['DELETE'])
@check_webtoken(extra_token=True)
def delete(flip_id):
    Flip.delete(flip_id)

