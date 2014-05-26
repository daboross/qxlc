import htmlmin
from markupsafe import Markup

from qxlc import app


@app.template_filter("minify")
def minify_filter(s):
    return Markup(htmlmin.minify(str(s), remove_comments=True, remove_empty_space=True))
