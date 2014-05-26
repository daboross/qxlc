import codecs
import hashlib
import logging
import os

from flask import render_template, abort
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
        with  open(filepath, "xb", encoding="utf-8", errors="replace") as file:
            file.write(data)
    return "http://qx.lc/{}".format(encode_id(raw_id))


def view_paste(raw_id):
    filepath = os.path.join(paste_path, str(raw_id))
    if not os.path.exists(filepath):
        return abort(404)
    with codecs.open(filepath, encoding="utf-8", errors="replace") as file:
        data = file.read()
        return render_template("paste.html", paste_data=data)
