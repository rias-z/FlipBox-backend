from flask import Blueprint, jsonify, make_response, request

from app.models.good import Good
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('good', __name__)

