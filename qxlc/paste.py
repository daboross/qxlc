import codecs
import hashlib
import logging
import os

import cssmin

from flask import render_template, abort
from flask.globals import request
from flask.wrappers import Response
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from qxlc import app
from qxlc.database import encode_id, store_data

paste_path = os.path.join(os.path.abspath("data"), "pastes")

if not os.path.exists(paste_path):
    os.makedirs(paste_path)
    logging.info("Created directory {}".format(paste_path))

_formatter = HtmlFormatter(linenos="table")
_highlight_css = cssmin.cssmin(_formatter.get_style_defs("body"))


@app.route("/api/paste", methods=["POST"])
def action_paste():
    if not "paste" in request.form:
        return "Missing form data: paste", 400
    data = request.form["paste"].strip()
    logging.info("Got data {}".format(data))
    raw_id = store_data("paste", hashlib.md5(data.encode()).hexdigest())  # use md5sum as data to detect duplicates
    filepath = os.path.join(paste_path, str(raw_id))
    if not os.path.exists(filepath):
        with codecs.open(filepath, "xb", encoding="utf-8", errors="replace") as file:
            file.write(data)
    return "http://qx.lc/{}".format(encode_id(raw_id))


def view_paste(raw_id, file_extension=None):
    filepath = os.path.join(paste_path, str(raw_id))
    if not os.path.exists(filepath):
        return abort(404)
    with codecs.open(filepath, encoding="utf-8", errors="replace") as file:
        data = file.read()

    try:
        if file_extension is not None:
            lexer = get_lexer_for_filename("*." + file_extension, code=data)
        else:
            lexer = guess_lexer(data)
    except ClassNotFound:
        lexer = TextLexer()

    return render_template("paste.html", paste_data=highlight(data, lexer, _formatter))


@app.route("/css/highlight.css")
def highlight_css():
    return Response(_highlight_css, mimetype="text/css")
