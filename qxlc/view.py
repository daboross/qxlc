from flask import render_template, redirect, abort
from flask.wrappers import Response

from qxlc import app, paste
from qxlc.database import get_data, decode_id, type_id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<encoded_id>")
@app.route("/<encoded_id>.<file_extension>")
def get_result(encoded_id, file_extension=None):
    if len(encoded_id) != 4:
        # all of our encoded ids are 4 characters long, so we can just 404 anything else.
        return abort(404)
    try:
        raw_id = decode_id(encoded_id)
        data_type, data = get_data(raw_id)
    except ValueError:
        # ValueError will also catch errors in decode_id if the id is invalid.
        # we just want to respond with 404 for all invalid or not found ids.
        return abort(404)

    if data_type == type_id("url"):
        return redirect(data)
    elif data_type == type_id("paste"):
        return paste.view_paste(encoded_id, raw_id, file_extension=file_extension)

    # we don't know about this id type, why is it in our database?
    raise ValueError("Invalid data_type: {}".format(data_type))


@app.route("/raw/<encoded_id>")
def get_raw(encoded_id):
    if len(encoded_id) != 4:
        # all of our encoded ids are 4 characters long, so we can just 404 anything else.
        return abort(404)
    try:
        raw_id = decode_id(encoded_id)
        data_type, data = get_data(raw_id)
    except ValueError:
        # ValueError will also catch errors in decode_id if the id is invalid.
        # we just want to respond with 404 for all invalid or not found ids.
        return abort(404)
    if data_type == type_id("url"):
        return Response(data, mimetype="text/plain")
    elif data_type == type_id("paste"):
        return paste.raw_paste(raw_id)