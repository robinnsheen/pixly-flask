"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Picture(db.Model):
    """Picture in the system"""

    __tablename__ = 'pictures'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
