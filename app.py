import os
from unittest.mock import seal
from dotenv import load_dotenv
from flask import (
    Flask, jsonify, render_template, url_for, request, flash, redirect, session, abort,
)
from werkzeug.utils import secure_filename


from flask_debugtoolbar import DebugToolbarExtension
# from aws import Aws

import json

from forms import (
    PictureAddForm
)
from models import (
    db, connect_db, Picture, )

from helpers import (upload_pic, get_exif, allowed_file,
                     filter, BUCKET_NAME, REGION)

load_dotenv()


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get('/')
def homepage():
    """Show homepage and render base.html"""

    return redirect('/pictures')


@app.route('/add', methods=["GET", "POST"])
def upload_picture():
    """ Add a picture:

    Show form if GET. If valid form submission,
    Upload a picture from form to aws bucket and add a picture to the database

    If filename is empty, redirect to /add.
    Otherwise Redirect to /pictures
    """

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
                          obj_name=filename
                          )
            db.session.add(pic)
            db.session.commit()

        return redirect('/pictures')
    else:
        return render_template('addform.html', form=form)


@app.get('/pictures')
def get_pictures():
    """Show pictures. Render pictures.html with all pictures in database"""
    pictures = Picture.query.all()

    return render_template('pictures.html', pictures=pictures)


@app.get('/pictures/<int:id>')
def get_picture(id):
    """Show a picture with list of exif data. Renders picture.html"""

    picture = Picture.query.get_or_404(id)
    exifs = json.loads(picture.exif)

    return render_template('picture.html', picture=picture, exifs=exifs)


@app.post('/pictures/<int:id>')
def filter_image(id):
    """Filter a picture and redirect to /pictures/<int:id>"""

    filterType = request.form['filter']
    picture = Picture.query.get_or_404(id)
    filter(picture, filterType)
    return redirect(f'/pictures/{id}')


@app.post('/pictures/delete/<int:id>')
def delete_image(id):
    """Delete a picture from database and redirect to /pictures"""
    pic = Picture.query.get_or_404(id)
    db.session.delete(pic)
    db.session.commit()
    return redirect("/pictures")


@app.get('/pictures/search')
def search():
    search_term = request.args['search']
    result = db.session.execute(
        f"SELECT * FROM pictures WHERE ts @@ to_tsquery(:term)", {"term": search_term})

    return render_template('pictures.html', pictures=result)
