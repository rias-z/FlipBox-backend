from flask import Blueprint, jsonify, make_response, request

from app.models.flip import Flip
from app.models.flip_item import FlipItem
from app.models.flip_tag import FlipTag
from app.models.item import Item
from app.models.tag import Tag
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('flip', __name__)


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
        print(token_data)
        flip = Flip.post(request.data.flip)
        for i in request.data.items:
            item = Item.post(i)
            params = {'flip_id': flip.id, 'item_id': item.id}
            FlipItem.post(params)

        for i in request.data.tags:
            tag = Tag.post(i)
            params = {'flip_id': flip.id, 'tag_id': tag.id}
            FlipTag.post(params)

        items = FlipItem.get_by_flip_id(flip.id)
        tags = FlipTag.get_by_flip_id(flip.id)

        result = {'flip': flip, 'items': items, 'tags': tags}
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/flip', methods=['PUT'])
@check_webtoken(extra_token=True)
def put(token_data):
    try:
        print(token_data)
        flip = Flip.put(request.data.flip)
        for i in request.data.items:
            item = Item.put(i)
            params = {'flip_id': flip.id, 'item_id': item.id}
            FlipItem.put(params)

        for i in request.data.tags:
            tag = Tag.put(i)
            params = {'flip_id': flip.id, 'tag_id': tag.id}
            FlipTag.put(params)

        items = FlipItem.get_by_flip_id(flip.id)
        tags = FlipTag.get_by_flip_id(flip.id)

        result = {'flip': flip, 'items': items, 'tags': tags}
        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


@app.route('/flip/<flip_id>', methods=['DELETE'])
@check_webtoken(extra_token=True)
def delete(flip_id):
    Flip.delete(flip_id)

