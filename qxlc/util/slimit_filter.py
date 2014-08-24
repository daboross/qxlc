from slimit import minify
from webassets.filter import Filter


class SlimitFilter(Filter):
    name = 'slimit'

    def output(self, _in, out, **kwargs):
        out.write(minify(_in.read()))

    def input(self, _in, out, **kwargs):
        out.write(_in.read())
