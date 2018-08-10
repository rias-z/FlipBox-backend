from flask import Blueprint, jsonify, make_response, request

from app.models.flip import Flip
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('flip', __name__)
