from flask import Blueprint
from . import Emailer

bp = Blueprint('email', __name__, template_folder='templates')



