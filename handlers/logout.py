
""" Module classes:
LogoutHandler - Handler for logging out.
"""

from base import BaseHandler

##############################################################################

class LogoutHandler(BaseHandler):
    """Handler for logging out."""

    def get(self):
        if self.logged_in():
            # Clear the Cookie:
            self.response.set_cookie("user_id", "", path="/")
            self.render("logout.html")
        else:
            self.render("index.html")