from flask import Blueprint, jsonify, make_response, request

from app.models.tag import Tag
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('tag', __name__)

