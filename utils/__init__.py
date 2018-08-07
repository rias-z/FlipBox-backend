import sys


def usage_exit():
    msg = []
    msg.append('usage: server.py [-h ] [-e]\n')
    sys.exit(0)


def get_in(_dict, *paths):
    item = _dict
    for path in paths:
        item = item.get(path)
        if item is None:
            return None

    return item
