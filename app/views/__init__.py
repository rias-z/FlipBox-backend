from . import (
    auth,
    comment,
    user,
)


blueprints = [
    auth.app,
    comment.app,
    user.app,
]


def get_blueprints():
    return blueprints
