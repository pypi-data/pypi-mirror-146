import jinja2
from jinja2.ext import Extension

from .templatetags.shatailuserbar import shatailuserbar


class ShatailUserbarExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update(
            {
                "shatailuserbar": jinja2.pass_context(shatailuserbar),
            }
        )


# Nicer import names
userbar = ShatailUserbarExtension
