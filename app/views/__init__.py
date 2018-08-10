from . import (
    auth,
    comment,
    bookmark,
    user,
)


blueprints = [
    auth.app,
    comment.app,
    bookmark.app,
    user.app,
]


def get_blueprints():
    return blueprints
