from flask import Blueprint, jsonify, make_response, request

from app.models.follow import Follow
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('follow', __name__)

