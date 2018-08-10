from flask import Blueprint, jsonify, make_response, request

from app.models.flip_tag import FlipTag
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('flip_tag', __name__)

