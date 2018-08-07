import functools

from flask import make_response, request

from app.views.utils.auth import check_and_decode_webtoken


def check_webtoken(func=None, extra_token=False):
    '''
    MEMO:
        webtokenをデコードしたtoken_dataを使う場合，以下の引数を追加する

        @check_webtoken(extra_token=True)
        def get(id, token_data):
            ...
    '''
    if func is None:
        return functools.partial(check_webtoken, extra_token=extra_token)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Authorization Bearerチェック
        Returns:
            403: 認証エラー（token不正，期限切れ）
        """
        try:
            token = request.headers['Authorization'].split()[1]

            # bearer token取得失敗
            if token is None:
                return make_response('', 403)

            token_data = check_and_decode_webtoken(token)

            # tokenの有効期限が切れていた場合
            if token_data is None:
                return make_response('', 403)

            if extra_token:
                kwargs.update({
                    'token_data': token_data
                })

            return func(*args, **kwargs)

        except Exception as e:
            return make_response('', 403)

    return wrapper
