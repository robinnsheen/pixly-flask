import os
from dotenv import load_dotenv

from flask import (
    Flask, url_for, request, flash, redirect, session, abort,
)
from werkzeug.utils import secure_filename


from flask_debugtoolbar import DebugToolbarExtension

from forms import (
    PictureAddForm
)
from models import (
    db, connect_db, Picture, )

UPLOAD_FOLDER = './imgs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

load_dotenv()

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
toolbar = DebugToolbarExtension(app)

connect_db(app)
