import logging
import traceback

from flask import render_template

from qxlc import app, push, device


@app.route("/500")
@app.errorhandler(Exception)
def internal_error(exception=None):
    if exception is not None:
        # We're actually handling an exception, not /500
        logging.exception("500 Exception")
        try:
            # exception notices!
            if push is not None:
                push.push_note(device, "QXLC Exception", traceback.format_exc())
        except Exception:
            pass

    return render_template("500.html"), 500


@app.route("/404")
@app.errorhandler(404)
def page_not_found(unused=None):
    return render_template("404.html"), 404


@app.route("/403")
@app.errorhandler(403)
def unauthorized(unused=None):
    return render_template("403.html"), 403
