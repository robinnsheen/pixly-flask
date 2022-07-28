"""SQLAlchemy models for Pixly."""

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

db = SQLAlchemy()

DEFAULT_IMAGE_URL = (
    "https: // my-bucket-laithabdz.s3.amazonaws.com/default-placeholder.png")


class Picture(db.Model):
    """Picture in the system"""

    __tablename__ = 'pictures'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    url = db.Column(
        db.Text,
        unique=True,
        default=DEFAULT_IMAGE_URL,
    )

    exif = db.Column(
        db.Text,
    )

    obj_name = db.Column(
        db.Text,
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
