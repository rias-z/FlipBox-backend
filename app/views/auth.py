from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, make_response, request

from app.config import current_config
from app.models.provisional_user import ProvisionalUser
from app.models.user import User
from app.views.utils.mail import send_confirm_mail
from app.views.utils.auth import generate_token


app = Blueprint('auth', __name__)

JST = timezone(timedelta(hours=+9), 'JST')


# TODO パラメータのバリデーション #5
@app.route('/auth/login', methods=['POST'])
def login():
    '''ユーザの仮登録を行う
    Args:
        email:  学番メール
        password:  学番メール
    Returns:
        200:    正常にログイン
        400:    ログイン失敗（存在しないメールアドレス，間違ったパスワード）
        500:    サーバエラー
    '''
    try:
        params = request.json

        email = params.get('email')
        password = params.get('password')

        # ユーザ照合
        user = User.login(email, password)

        # メールアドレスとパスワードが一致しない場合，400を返す
        if not user:
            return make_response('', 400)

        # アクセストークン発行
        web_token = generate_token(user.get('user_id'), email)

        result = {
            'web_token': web_token
        }

        return make_response(jsonify(result), 200)
    except Exception as e:
        return make_response('', 500)


# TODO パラメータのバリデーション #5
@app.route('/auth/prov_user', methods=['POST'])
def register_prov_user():
    '''ユーザの仮登録を行う
    Args:
        email:  学番メール
    Returns:
        200:    正常に登録が行われた
        400:    不正なメールアドレス
        500:    サーバエラー
    '''
    try:
        params = request.json

        email = params.get('email')

        # 仮登録を行う
        # トークンを返却
        # TODO 仮登録を連続で登録できないようにinterva_timeを設定する
        login_token = ProvisionalUser.post(email)

        mail = current_config('mail')

        # 確認メール送信
        send_confirm_mail(
            from_addr=mail.get('address'),
            from_addr_pass=mail.get('pass'),
            to_addr=email,
            login_token=login_token
        )

        return make_response('', 200)
    except Exception as e:
        if str(e) == 'over email length':
            result = {
                'error_message': 'メールが長すぎます'
            }
            return make_response(jsonify(result), 400)

        return make_response('', 500)


# TODO パラメータのバリデーション #5
@app.route('/auth/register', methods=['POST'])
def register():
    '''ユーザの本登録を行う
    Args:
        * login_token:  仮登録のトークン
        * password:     パスワード
        * nick_name:    ニックネーム
        profile:        プロファイル
        twitter_name:   ツイッターネーム
    Returns:
        201:    正常登録
        400:    仮登録ユーザが存在しない，トークンの有効期限切れ，トークンの不一致
            error_message:  エラーメッセージ（必要なエラーのみ）
        500:    サーバエラー

    * 必須
    '''
    try:
        params = request.json

        nick_name = params.get('nick_name')
        login_token = params.get('login_token')

        # login_tokenからemailを取得する
        prov_user = ProvisionalUser.get_by_login_token(login_token=login_token)

        # 仮登録ユーザが存在しない場合，400を返却
        if not prov_user:
            result = {
                'error_message': '仮登録を行なってください'
            }
            return make_response(jsonify(result), 400)

        email = prov_user.get('email')

        # emailが既に本登録されているか
        if User.is_exist_by_email(email):
            # ユーザが登録されている場合，400を返す
            result = {
                'error_message': 'このメールアドレスは既に使われています'
            }
            return make_response(jsonify(result), 400)

        # 仮登録作成時間と現在時間の差分を取得
        delta = datetime.now(JST) - prov_user['create_at']

        prov_expire_time = current_config('prov_expire_time')

        # 有効時間切れの場合，400を返却
        if delta.total_seconds() > prov_expire_time:
            result = {
                'error_message': 'リンクの有効期限切れです'
            }
            return make_response(jsonify(result), 400)

        # トークンが不一致の場合，400を返却
        if login_token != prov_user['login_token']:
            result = {
                'error_message': 'リンクの有効期限切れです'
            }
            return make_response(jsonify(result), 400)

        # paramsからlogin_token除去
        del params['login_token']

        # paramsにemail追加
        params.update({
            'email': email
        })

        # ユーザ本登録
        User.post(params)

        return make_response('', 201)
    except Exception as e:
        return make_response('', 500)
