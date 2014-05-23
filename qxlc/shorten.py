from flask.globals import request

from flask.templating import render_template

from qxlc import app

from qxlc.database import encode_id, decode_id, store_data


@app.route("/api/shorten", methods=["POST"])
def action_short():
    params = request.args
    if not "url" in params:
        return "Missing parameter: url", 400
    if not "api_key" in params:
        return "Missing parameter: api_key", 400
    url = params["url"]

    return "http://qx.lc/{}".format(encode_id(store_data("url", url)))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<encoded_id>")
def get_result(encoded_id):

    return str(decode_id(encoded_id)), 400
