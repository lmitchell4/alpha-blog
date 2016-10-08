
""" Module classes:
MainHandler - Handler for the web site home page.
"""

from base import BaseHandler
from models.user import UserAccount

##############################################################################

class MainHandler(BaseHandler):
    """Handler for the web site home page."""

    def get(self):
        all_users = UserAccount.get_all_usernames()
        if all_users:
            self.render("index.html",
                        account=self.account,
                        usernames=all_users)
        else:
            self.render("index.html",
                        account=self.account)
