from flask import request

from qxlc import app
from qxlc.paste import paste_data
from qxlc.shorten import valid_url, shorten_url


@app.route("/api/generic-submit", methods=["POST"])
def action_submit_generic():
    if not "content" in request.form:
        return "Missing form data: content", 400
    data = request.form["content"].strip()
    if valid_url.match(data):
        return shorten_url(data)
    else:
        return paste_data(data)
