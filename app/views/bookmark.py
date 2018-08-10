from flask import Blueprint, jsonify, make_response, request

from app.models.bookmark import Bookmark
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('bookmark', __name__)

