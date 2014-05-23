import re

from flask import redirect

from flask.globals import request
from flask.templating import render_template

from qxlc import app

from qxlc.database import encode_id, decode_id, store_data, get_data, type_id

valid_url = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


@app.route("/api/shorten", methods=["POST"])
def action_short():
    params = request.args
    if not "url" in params:
        return "Missing parameter: url", 400
    if not "api_key" in params:
        return "Missing parameter: api_key", 400
    url = params["url"]
    if not valid_url.match(url):
        return "Invalid URL", 400
    return "http://qx.lc/{}".format(encode_id(store_data("url", url)))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<encoded_id>")
def get_result(encoded_id):
    if len(encoded_id) != 4:
        # all of our encoded ids are 4 characters long, so we can just 404 anything else.
        return render_template("404.html"), 404

    try:
        data_type, data = get_data(decode_id(encoded_id))
    except ValueError:
        # ValueError will also catch errors in decode_id if the id is invalid.
        # we just want to respond with 404 for all invalid or not found ids.
        return render_template("404.html"), 404

    if data_type == type_id("url"):
        return redirect(data)

    # we don't know about this id type, why is it in our database?
    raise ValueError("Invalid data_type: {}".format(data_type))
