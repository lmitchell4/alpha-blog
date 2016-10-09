
""" Module classes:
SignupHandler - Handler for the signup page.
"""

from base import BaseHandler

from models.user import UserAccount

import validation

##############################################################################

class SignupHandler(BaseHandler):
    """Handler for the signup page."""

    def get(self):
        if self.logged_in():
            self.render("error.html", account=self.account)
        else:
            self.render("signup.html")

    def post(self):
        form_ok = True

        # Retrieve user data and strip white space from front and back:
        self.username = self.request.get("username").strip()
        self.password = self.request.get("password").strip()
        self.verify = self.request.get("verify").strip()
        self.email = self.request.get("email").strip()

        display_data = dict(username = self.username,
                            email = self.email)

        # Check username:
        if not validation.valid_username(self.username):
            display_data["username_error"] = "That's not a valid username."
            form_ok = False

        # Check password:
        if not validation.valid_password(self.password):
            display_data["password_error"] = "That's not a valid password."
            form_ok = False
        elif self.password != self.verify:
            display_data["verify_error"] = "Your passwords didn't match."
            form_ok = False

        # Only check email if there is an email:
        if self.email != "":
            if not validation.valid_email(self.email):
                display_data["email_error"] = "That's not a valid email."
                form_ok = False

        if form_ok:
            self.done(display_data)
        else:
            # Re-render, keeping the username and email:
            self.render("signup.html", **display_data)

    def done(self, display_data):
        user = UserAccount.by_username(self.username)

        if user:
            display_data["username_error"] = "That user already exists."
            self.render("signup.html", **display_data)
        else:
            # Create new datastore entity, set secure Cookie for this
            # user, and redirect to the user's home page.
            user = UserAccount.create(self.username,
                                      self.password,
                                      self.email)
            self.set_secure_userid_cookie(user)
            # # self.redirect("/home", user.username)
            
            # # self.render("home.html", author = user.username)
            self.redirect("/home/%s" % user.username)
