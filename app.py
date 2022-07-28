import os
from dotenv import load_dotenv
from flask import (
    Flask, jsonify, render_template, url_for, request, flash, redirect, session, abort,
)
from werkzeug.utils import secure_filename

from PIL import Image
from urllib. request import urlopen
from flask_debugtoolbar import DebugToolbarExtension
# from aws import Aws

import json

from forms import (
    PictureAddForm
)
from models import (
    db, connect_db, Picture, )
import logging
import boto3
from botocore.exceptions import ClientError


from PIL.ExifTags import TAGS

load_dotenv()

BUCKET_NAME = os.environ['BUCKET_NAME']
REGION = os.environ['REGION']
UPLOAD_FOLDER = './imgs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres:///", "postgresql:///"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)


def get_exif(file):
    exif = {}
    url_open = urlopen(
        f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{file.filename}")

    # getting metadata
    img = Image.open(
        url_open)
    exifdata = img.getexif()

    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)

        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        exif[f"{tag}"] = f"{data}"
    return exif


def upload_pic(file, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file
    if object_name is None:
        object_name = os.path.basename(file)

    # Upload the filse
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(file, bucket, object_name,
                                 ExtraArgs={
                                     'ACL': 'public-read'}
                                 )
    except ClientError as e:
        logging.error(e)
        return False


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get('/')
def homepage():

    return render_template('base.html')


@app.route('/add', methods=["GET", "POST"])
def upload_picture():

    form = PictureAddForm()

    if form.validate_on_submit():
        file = request.files['file']
        name = form.name.data

        if file.filename == "":
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_pic(file, BUCKET_NAME, filename)
            exif = get_exif(file)
            json_exif = json.dumps(exif)

            pic = Picture(name=name,
                          url=f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{file.filename}",
                          exif=json_exif,
                          )
            db.session.add(pic)
            db.session.commit()

        return redirect('/pictures')
    else:
        return render_template('addform.html', form=form)


@app.get('/pictures')
def get_pictures():
    pictures = Picture.query.all()

    return render_template('pictures.html', pictures=pictures)


@app.get('/pictures/<int:id>')
def get_picture(id):

    picture = Picture.query.get_or_404(id)
    exifs = json.loads(picture.exif)

    return render_template('picture.html', picture=picture, exifs=exifs)
