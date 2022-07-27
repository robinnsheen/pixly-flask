import os
from dotenv import load_dotenv
from flask import (
    Flask, render_template, url_for, request, flash, redirect, session, abort,
)
from werkzeug.utils import secure_filename


from flask_debugtoolbar import DebugToolbarExtension
# from aws import Aws

from forms import (
    PictureAddForm
)
from models import (
    db, connect_db, Picture, )
import logging
import boto3
from botocore.exceptions import ClientError

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
            # file.save(filename)

            upload_pic(file, BUCKET_NAME, filename)
            # return {"message": "success"}

        pic = Picture(name=name,
                      url=f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{file.filename}"
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
