import os
from dotenv import load_dotenv

import logging
import boto3
from botocore.exceptions import ClientError

from PIL import Image, ImageFilter
from urllib. request import urlopen
from PIL.ExifTags import TAGS

from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)

BUCKET_NAME = os.environ['BUCKET_NAME']
REGION = os.environ['REGION']
UPLOAD_FOLDER = './imgs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


load_dotenv()


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

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(file, bucket, object_name,
                                 ExtraArgs={
                                     'ACL': 'public-read'}
                                 )
    except ClientError as e:
        logging.error(e)
        return False


def get_exif(file):
    """Get exif data from a file and returns a dictionary
    with the data associated with exif tags.

    Return: {ResolutionUnit: 2, ...}

    """
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


def allowed_file(filename):
    """Check if file has extension in list of allowed extensions.
    Returns bool
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def filter(file):



    pic = open(filename, mode='r', buffering=-1, encoding=None,
               errors=None, newline=None, closefd=True, opener=None)

    url_open = urlopen(file.url)

    im = Image.open(
        url_open)
    im1 = im.filter(ImageFilter.BLUR)

    im2 = im.filter(ImageFilter.MinFilter(3))

    im3 = im.filter(ImageFilter.MinFilter)

    upload_pic(im3, BUCKET_NAME)
