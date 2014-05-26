import hashlib
import logging
import os

from flask.globals import request

from qxlc import app
from qxlc.database import encode_id, store_data

paste_path = os.path.join(os.path.abspath("data"), "pastes")

if not os.path.exists(paste_path):
    os.makedirs(paste_path)
    logging.info("Created directory {}".format(paste_path))

@app.route("/api/paste", methods=["POST"])
def action_paste():
    if not "paste" in request.form:
        return "Missing form data: paste", 400
    data = request.form["paste"].strip()
    logging.info("Got data {}".format(data))
    raw_id = store_data("paste", hashlib.md5(data.encode()).hexdigest())  # use md5sum as data to detect duplicates
    filepath = os.path.join(paste_path, str(raw_id))
    if not os.path.exists(filepath):
        with open(filepath, "x") as file:
            file.write(data)
    return "http://qx.lc/{}".format(encode_id(raw_id))


def view_paste(raw_id):
    filepath = os.path.join(paste_path, str(raw_id))
    with open(filepath) as file:
        return file.read()
