import re

from flask.globals import request

from qxlc import app, base_url
from qxlc.database import encode_id, store_data

valid_url = re.compile(
    r'^(?:(?:http|ftp)s?://)?'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

url_with_protocol = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


@app.route("/api/shorten", methods=["POST"])
def action_short():
    params = request.args
    if request.method == "GET":
        params = request.args
    elif request.method == "POST":
        params = request.form

    if not "url" in params:
        return "Missing parameter: url", 400
    url = params["url"]
    return shorten_url(url)


def shorten_url(url):
    if not valid_url.match(url):
        return "Invalid URL", 400
    if not url_with_protocol.match(url):
        url = "http://{}".format(url)
    return "{}/{}".format(base_url, encode_id(store_data("url", url)))
