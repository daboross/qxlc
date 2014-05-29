import codecs
import hashlib
import logging
from operator import itemgetter
import os
import re

import cssmin
from flask import render_template, abort
from flask.globals import request
from flask.wrappers import Response
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_for_filename, get_all_lexers
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from qxlc import app, base_url
from qxlc.database import encode_id, store_data

paste_path = os.path.join(os.path.abspath("data"), "pastes")

if not os.path.exists(paste_path):
    os.makedirs(paste_path)
    logging.info("Created directory {}".format(paste_path))

_formatter = HtmlFormatter(linenos="table")
_highlight_css = cssmin.cssmin(_formatter.get_style_defs("body"))

_all_lexers = sorted([(l[0], l[2][0]) for l in get_all_lexers() if l[2]], key=itemgetter(0))
_all_lexers = [(title, extension[2:]) for title, extension in _all_lexers if
               len(title.split()) == 1 and re.match(r"^\*\.[a-zA-Z0-9]+$", extension)]


@app.route("/api/paste", methods=["POST"])
def action_paste():
    if not "paste" in request.form:
        return "Missing form data: paste", 400
    data = request.form["paste"].strip()
    raw_id = store_data("paste", hashlib.md5(data.encode()).hexdigest())  # use md5sum as data to detect duplicates
    filepath = os.path.join(paste_path, str(raw_id))
    if not os.path.exists(filepath):
        with codecs.open(filepath, "xb", encoding="utf-8", errors="replace") as f:
            f.write(data)
    return "{}/{}".format(base_url, encode_id(raw_id))


def view_paste(encoded_id, raw_id, file_extension=None):
    filepath = os.path.join(paste_path, str(raw_id))
    if not os.path.exists(filepath):
        return abort(404)
    with codecs.open(filepath, encoding="utf-8", errors="replace") as f:
        data = f.read()

    try:
        if file_extension is not None:
            lexer = get_lexer_for_filename("*." + file_extension, code=data)
        else:
            lexer = guess_lexer(data)
    except ClassNotFound:
        lexer = TextLexer()

    return render_template("paste.html", lexers=_all_lexers,
                           lexer_url="{}/{}.".format(base_url, encoded_id),
                           raw_url="{}/raw/{}".format(base_url, encoded_id),
                           current_lexer=lexer.name,
                           paste_data=highlight(data, lexer, _formatter))


def raw_paste(raw_id):
    filepath = os.path.join(paste_path, str(raw_id))
    if not os.path.exists(filepath):
        return abort(404)
    with codecs.open(filepath, encoding="utf-8", errors="replace") as f:
        data = f.read()

    return Response(data, mimetype="text/plain")


@app.route("/css/highlight.css")
def highlight_css():
    return Response(_highlight_css, mimetype="text/css")
