from flask import Blueprint, jsonify, make_response, request

from app.models.user_notify import UserNotify
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('user_notify', __name__)

