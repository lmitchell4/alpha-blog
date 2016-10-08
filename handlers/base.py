
""" Module classes:
BaseHandler - Handler for rendering templates and manipulating Cookies.

This project is based on code developed by Udacity.
"""

import os
import time

import webapp2
import jinja2

import validation
from models.user import UserAccount
from models.post import BlogEntry

##############################################################################
## Define jinja2 templates:

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

##############################################################################

class BaseHandler(webapp2.RequestHandler):
    """Handler for rendering templates and manipulating Cookies."""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params["user"] = self.user
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        # Generic version.
        secure_cookie_val = validation.make_secure_val(val)
        self.response.headers.add_header(
            "Set-Cookie",
            "%s=%s; Path=/" % (name, secure_cookie_val)
        )

    def set_secure_userid_cookie(self, user):
        # Specifically for setting user_id.
        self.set_secure_cookie("user_id", str(user.key.id()))

    def read_secure_cookie(self, name):
        secure_cookie_val = self.request.cookies.get(name)
        if secure_cookie_val:
            return validation.check_secure_val(secure_cookie_val)
        else:
            return None

    def logout(self):
        self.response.set_cookie("user_id", "", path="/")

    def initialize(self, *a, **kw):
        # This gets run before every request handler to check that the
        # user is still logged in.
        # Check that the Cookie is valid and return the user if they are
        # found in the datastore.
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie("user_id")
        self.user = uid and UserAccount.by_id(int(uid))

        self.account = None
        if self.user:
            self.account = self.user.username

        author = self.request.get("author")
        if author:
            self.author = author
        else:
            self.author = ""

    def logged_in(self):
        """ Return True if someone is logged in to the site.
            This will always get called after initialize, so it should
            reflect whether or not someone is logged in with a valid cookie.
        """
        if self.account:
            return True
        else:
            return False

    def user_and_author(self):
        """ Return True if someone is logged in AND the person logged in
            is the author of the current blog.
        """
        if self.logged_in() and self.account == self.author:
            return True
        else:
            return False
