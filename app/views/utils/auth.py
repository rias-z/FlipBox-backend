import time
import jwt

from app.config import current_config


def check_and_decode_webtoken(token):
    try:
        d_token = decode_token(token)

        # アクセストークンの有効期限が切れていた場合，400を返す
        if d_token['expire'] < time.time():
            return None

        return d_token
    except: # NOQA
        raise Exception('failed decode token')


def generate_token(user_id, email):
    login_expire_time = current_config('login_expire_time')

    token_data = {
        'user_id': user_id,
        'email': email,
        'expire': time.time() + login_expire_time
    }

    secret_key = current_config('secret_key')
    algorithm = current_config('algorithm')

    token = _jwt_encode(
        token_data,
        secret=secret_key,
        algorithm=algorithm
    )

    return token.decode()


def decode_token(token):
    secret_key = current_config('secret_key')

    token_data = _jwt_decode(token, secret=secret_key)

    if token_data is None:
        raise Exception('invalid token')
    else:
        return token_data


def _jwt_encode(dict_data, secret, algorithm):
    return jwt.encode(dict_data, secret, algorithm=algorithm)


def _jwt_decode(encoded, secret):
    try:
        token = jwt.decode(encoded, secret)
    except jwt.exceptions.DecodeError as e:
        token = None

    return token
