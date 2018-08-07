from . import (
    auth,
    category,
    comment,
    sort,
    thread,
    university,
    user,
)


blueprints = [
    auth.app,
    category.app,
    comment.app,
    sort.app,
    thread.app,
    university.app,
    user.app,
]


def get_blueprints():
    return blueprints
