from flask import Blueprint, jsonify, make_response, request

from app.models.provisional_user import ProvisionalUser
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('provisional_user', __name__)

