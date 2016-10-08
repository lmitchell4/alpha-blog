
""" Module classes:
LogoutHandler - Handler for logging out.
"""

from base import BaseHandler

##############################################################################

class LogoutHandler(BaseHandler):
    """Handler for logging out."""

    def get(self):
        # Clear the Cookie and redirect:
        self.response.set_cookie("user_id", "", path="/")
        self.render("logout.html")
