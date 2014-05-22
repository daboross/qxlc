from flask.templating import render_template
from qxlc import app

@app.route("/actions/short", methods=["POST"])
def paste():
    raise ValueError

@app.route("/actions/paste", methods=["POST"])
def paste():
    raise ValueError

@app.route("/")
def index():
    return render_template("index.html")