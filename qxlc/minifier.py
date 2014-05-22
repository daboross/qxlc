import htmlmin
from markupsafe import Markup

from qxlc import app


@app.template_filter("minify")
def minify_filter(text):
    return Markup(htmlmin.minify(text.unescape(), remove_comments=True, remove_empty_space=True))
