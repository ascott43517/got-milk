from flask import Blueprint, request, jsonify, make_response
from app import db

hello_bp = Blueprint("homepage", __name__,url_prefix="/")
posts_bp = Blueprint("posts", __name__, url_prefix="/posts")
users_bp = Blueprint("users", __name__, url_prefix="/users")

