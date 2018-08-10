from flask import Blueprint, jsonify, make_response, request

from app.models.notify import Notify
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('notify', __name__)

