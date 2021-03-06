
""" Module classes:
LoginHandler - Handler for the login page.
"""

from base import BaseHandler

from models.user import UserAccount

##############################################################################

class LoginHandler(BaseHandler):
    """Handler for the login page."""

    def get(self):
        if self.logged_in():
            self.render("error.html", account=self.account)
        else:
            self.render("login.html")

    def post(self):
        if self.logged_in():
            self.render("error.html", account=self.account)
            return

        # Retrieve user data and strip white space from front and back:
        username = self.request.get("username").strip()
        password = self.request.get("password").strip()

        # Check login credentials:
        user = UserAccount.login(username, password)

        if user:
            # Set the secure Cookie for this user and redirect to
            # the user's home page.
            self.set_secure_userid_cookie(user)
            self.redirect("/home/%s" % user.username)

        else:
            # Username not found, or invalid password.
            self.render("login.html", username,
                        invalid_error = "Invalid login")
