import hashlib
import logging
import os
import shutil
import tempfile

from flask import abort
from flask.globals import request
from flask.helpers import send_file

from qxlc import app, base_url, config
from qxlc.database import encode_id, store_data

upload_path = os.path.join(os.path.abspath("data"), "images")
allowed_extensions = ["png", "jpg"]
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # allow up to 1 MiB TODO: configurable this

if not os.path.exists(upload_path):
    os.makedirs(upload_path)
    logging.info("Created directory {}".format(upload_path))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions


@app.route("/api/image", methods=["POST"])
def action_image():
    if not "image" in request.files:
        return "Missing file: image", 400
    if not "api_key" in request.form:
        return "Missing form data: api_key", 400
    if request.form["api_key"] != config.get("image_api_key", ""):
        return "Invalid api_key", 400
    file = request.files["image"]
    if not allowed_file(file.filename):
        return "Invalid filename: expected *.png, found {}".format(file.filename), 400

    # TODO: Load into memory, and ensure that it's a valid png file.
    with tempfile.NamedTemporaryFile(prefix=".temp-upload-", dir=upload_path, delete=False) as temp_file:
        md5sum = hashlib.md5()
        while True:
            data = file.read(1024)
            if data is None:
                logging.warning("None returned from file.read(1024)")
                continue
            if data == b'':
                break
            md5sum.update(data)
            temp_file.write(data)

    # use md5sum as data to detect duplicates
    raw_id = store_data("image", "image/" + file.filename.rsplit('.', 1)[1] + ":" + md5sum.hexdigest())

    filepath = os.path.join(upload_path, str(raw_id))

    if not os.path.exists(filepath):
        shutil.move(temp_file.name, filepath)
    else:
        os.remove(temp_file.name)

    return "{}/{}".format(base_url, encode_id(raw_id))


def raw_image(raw_id, data):
    filepath = os.path.join(upload_path, str(raw_id))
    if not os.path.exists(filepath):
        return abort(404)

    if ':' in data:
        extension = data.split(':')[0]
    else:
        extension = 'image/png'

    return send_file(filepath, mimetype=extension)

# TODO: make front for images like paste, and only use raw_image in the /raw/ url.
