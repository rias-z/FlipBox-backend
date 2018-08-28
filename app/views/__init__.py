from . import (
    auth,
    bookmark,
    comment,
    flip,
    flip_item,
    flip_tag,
    folder,
    follow,
    good,
    item,
    notify,
    provisional_user,
    tag,
    user,
    user_notify,
    top,
)


blueprints = [
    auth.app,
    bookmark.app,
    comment.app,
    flip.app,
    flip_item.app,
    flip_tag.app,
    folder.app,
    follow.app,
    good.app,
    item.app,
    notify.app,
    provisional_user.app,
    tag.app,
    user.app,
    user_notify.app,
    top.app,
]


def get_blueprints():
    return blueprints
