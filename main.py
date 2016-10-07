
""" Module classes:
BaseHandler - Handler for rendering templates and manipulating Cookies.
SignupHandler - Handler for the signup page.
LoginHandler - Handler for the login page.
LogoutHandler - Handler for logging out.
WelcomeHandler - Handler for a welcome page.
MainHandler - Handler for the web site home page.
BlogHandler - Handler for a user's home page.
NewPostHandler - Handler for creating a new blog post.
PostHandler - Handler for the web page for an individual blog post.
EditHandler - Handler for editing an existing blog post.
DeleteHandler - Handler for deleting an existing blog post.
NewCommentHandler - Handler for new comments.
UpdateCommentHandler - Handler for editing existing comments.
RateHandler - Handler for the Like and Dislike buttons.
"""

import os
import json
import time

import webapp2
import jinja2

import datastore
import inputcheck

##############################################################################
## Define jinja2 templates:

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


##########################################
## Basic Handler:

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
        secure_cookie_val = inputcheck.make_secure_val(val)
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
            return inputcheck.check_secure_val(secure_cookie_val)
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
        self.user = uid and datastore.UserAccount.by_id(int(uid))

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


##########################################
## Account Handlers:

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
        if not inputcheck.valid_username(self.username):
            display_data["username_error"] = "That's not a valid username."
            form_ok = False

        # Check password:
        if not inputcheck.valid_password(self.password):
            display_data["password_error"] = "That's not a valid password."
            form_ok = False
        elif self.password != self.verify:
            display_data["verify_error"] = "Your passwords didn't match."
            form_ok = False

        # Only check email if there is an email:
        if self.email != "":
            if not inputcheck.valid_email(self.email):
                display_data["email_error"] = "That's not a valid email."
                form_ok = False

        if form_ok:
            self.done(display_data)
        else:
            # Re-render, keeping the username and email:
            self.render("signup.html", **display_data)

    def done(self, display_data):
        user = datastore.UserAccount.by_username(self.username)

        if user:
            display_data["username_error"] = "That user already exists."
            self.render("signup.html", **display_data)
        else:
            # Create new datastore entity, set secure Cookie for this
            # user, and redirect to the user's home page.
            user = datastore.UserAccount.create(self.username,
                                                 self.password,
                                                 self.email)
            self.set_secure_userid_cookie(user)
            self.redirect("/blog?author=%s" % user.username)


class LoginHandler(BaseHandler):
    """Handler for the login page."""

    def get(self):
        if self.logged_in():
            self.render("error.html", account=self.account)
        else:
            self.render("login.html")

    def post(self):
        # Retrieve user data and strip white space from front and back:
        username = self.request.get("username").strip()
        password = self.request.get("password").strip()

        # Check login credentials:
        user = datastore.UserAccount.login(username, password)

        if user:
            # Set the secure Cookie for this user and redirect to
            # the user's home page.
            self.set_secure_userid_cookie(user)
            self.redirect("/blog?author=%s" % user.username)

        else:
            # Username not found, or invalid password.
            display_data = dict(username = username,
                                invalid_error = "Invalid login")
            self.render("login.html", **display_data)


class LogoutHandler(BaseHandler):
    """Handler for logging out."""

    def get(self):
        # Clear the Cookie and redirect:
        self.response.set_cookie("user_id", "", path="/")
        self.render("logout.html")


class WelcomeHandler(BaseHandler):
    """Handler for a welcome page."""

    def get(self):
        if self.account:
            self.render("welcome.html", username=self.account)
        else:
            self.redirect("/signup")


##########################################
## Blog Handlers:

class MainHandler(BaseHandler):
    """Handler for the web site home page."""

    def get(self):
        all_users = datastore.UserAccount.get_all_usernames()
        if all_users:
            self.render("index.html",
                        account=self.account,
                        usernames=all_users)
        else:
            self.render("index.html",
                        account=self.account)


class BlogHandler(BaseHandler):
    """Handler for a user's home page.

       Currently not handling the Search button on this page.

    """

    def render_main(self, error_msg=""):
        blog_entries = datastore.BlogEntry.first_ten_list(self.author)

        # Get all rating information for this user and author:
        if blog_entries and self.logged_in():
            blog_entries = datastore.BlogEntry.add_ratings(
                entries=blog_entries,
                username=self.account)

        self.render("blog.html",
            account=self.account,
            author=self.author,
            blog_entries=blog_entries,
            error_msg=error_msg)

    def get(self):
        self.render_main()

    def post(self):
        action = self.request.get("newpost")
        if action == "New Post" and self.user_and_author():
            self.redirect("/blog/new")
        else:
            self.render_main("You must be logged in to your account " +
                             "to create a new blog post.")


class NewPostHandler(BaseHandler):
    """Handler for creating a new blog post."""

    def render_main(self, subject="", content="", error=""):
        self.render("newpost.html",
                    account=self.account,
                    author=self.account,
                    subject=subject,
                    content=content,
                    error=error)

    def get(self):
        self.render_main()

    def post(self):
        action = self.request.get("newpost-opt")

        if action == "Create":
            subject = self.request.get("subject").strip()
            content = self.request.get("content").strip()

            if subject and content:
                new_entry = datastore.BlogEntry.create(
                    author=self.account,
                    subject=subject,
                    content=content)
                self.redirect("/blog/post?author=%s&id=%s" %
                              (self.account, str(new_entry.key.id())))

            else:
                error = "Subject and content, please!"
                self.render_new(subject, content, error)

        elif action == "Cancel":
            self.redirect("/blog?author=%s" % self.account)


class PostHandler(BaseHandler):
    """Handler for the web page for an individual blog post.

       This must handle blog post editing/deleting, commenting,
       and rating capabilities.

    """

    def render_main(self, post_id, post_error="", get_new_comment = False,
                    new_comment_error="", update_target="",
                    update_comment_error=""):
        entry = datastore.BlogEntry.dict_by_id(int(post_id))
        comments = datastore.Comment.by_postid_dict(post_id)

        entry = datastore.BlogEntry.add_ratings(entries = [entry],
                                                 username = self.account)
        entry = entry[0]

        self.render("post.html",
                    account=self.account,
                    author=self.author,
                    entry=entry,
                    comments=comments,
                    post_error=post_error,
                    get_new_comment=get_new_comment,
                    new_comment_error=new_comment_error,
                    update_target=update_target,
                    update_comment_error=update_comment_error)

    def get(self):
        post_id = self.request.get("id")
        self.render_main(post_id=post_id)

    def post(self):
        author = self.request.get("author")
        post_id = self.request.get("id")

        # If the action is related to the post:
        action = self.request.get("changepost")
        if action:
            action = action.lower()
            if self.user_and_author():
                self.redirect("/blog/%s?author=%s&id=%s" %
                              (action, author, post_id))
            else:
                self.render_main(
                    post_id=post_id,
                    post_error="You can only %s your own posts." % action)
            return

        # If the action is related to a new comment:
        action = self.request.get("newcomment")
        if action:
            if self.logged_in():
                if action == "Add Comment":
                    self.render_main(post_id, get_new_comment=True)
                elif action == "Save":
                    self.save_comment(post_id, author)
                elif action == "Cancel":
                    self.redirect("/blog/post?author=%s&id=%s" %
                                  (author, post_id))

            else:
                self.render_main(
                    post_id,
                    get_new_comment=False,
                    new_comment_error="You must be logged in to comment.")
            return

        # If the action is related to an existing comment:
        action = self.request.get("updatecomment")
        if action:
            comment_id = self.request.get("comment_id")
            comment = datastore.Comment.by_id(int(comment_id))

            if comment.commenter == self.account:
                self.update_comment(post_id, author, comment_id, action)
            else:
                self.render_main(
                    post_id,
                    update_target=comment_id,
                    update_comment_error=
                        "You can only make changes to your own comments.")

    def save_comment(self, post_id, author):
        comment_content = self.request.get("comment-content").strip()

        if comment_content:
            # use author from the get parameters or from self.author?
            record = datastore.Comment.create(
                post_id=post_id,
                author=author,
                commenter=self.account,
                content=comment_content)
            time.sleep(0.1) # for now
            self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
        else:
            self.render_main(
                post_id,
                get_new_comment=True,
                new_comment_error="Comments can't be empty!")

    def update_comment(self, post_id, author, comment_id, action):
        if action == "Edit":
            self.render_main(post_id, update_target=comment_id)

        elif action == "Delete":
            # Delete from Comment datastore.
            datastore.Comment.delete_by_id(int(comment_id))
            time.sleep(0.1) # for now
            self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))

        elif action == "Save":
            new_content = self.request.get("comment-content").strip()
            if new_content:
                datastore.Comment.update(int(comment_id), new_content)
                time.sleep(0.1) # for now
                self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
            else:
                self.render_main(
                    post_id=post_id,
                    update_target=comment_id,
                    update_comment_error="Comments can't be empty!")

        elif action == "Cancel":
            self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))


class EditHandler(BaseHandler):
    """Handler for editing an existing blog post."""

    def render_main(self, post_id, error=""):
        entry = datastore.BlogEntry.dict_by_id(int(post_id))
        self.render("editpost.html",
                    account=self.account,
                    author=self.account,
                    entry=entry,
                    error=error)

    def get(self):
        post_id = self.request.get("id")
        self.render_main(post_id=post_id)

    def post(self):
        action = self.request.get("editpost-opt")

        if action == "Save":
            new_subject = self.request.get("subject")
            new_content = self.request.get("content").strip()

            if new_content:
                post_id = self.request.get("id")
                datastore.BlogEntry.update_by_id(
                    int(post_id),
                    new_subject, new_content)
                self.redirect("/blog/post?author=%s&id=%s" %
                              (self.author, post_id))

            else:
                self.render_main(post_id,
                                  error="Non-empty comment, please!")

        elif action == "Cancel":
            self.redirect("/blog?author=%s" % self.account)


class DeleteHandler(BaseHandler):
    """Handler for deleting an existing blog post.

       There is currently no option to undo a deletion.

    """
    def render_main(self, post_subject):
        self.render("delete.html",
                    account=self.account,
                    author=self.author,
                    post_subject=post_subject)

    def get(self):
        # Make sure the author is the one logged in.
        if self.user_and_author():
            # Delete the post and any associated comments.
            post_id = self.request.get("id")
            blog_entry = datastore.BlogEntry.get_by_id(int(post_id))
            post_subject = blog_entry.subject

            datastore.BlogEntry.delete_by_id(int(post_id))
            datastore.Comment.delete_all_by_postid(post_id)

            self.render_main(post_subject = post_subject)


class NewCommentHandler(BaseHandler):
    """Handler for new comments."""

    def render_main(self, post_id, get_new_comment=False, error=""):
        entry = datastore.BlogEntry.dict_by_id(int(post_id))
        comments = datastore.Comment.by_postid_dict(post_id)

        self.render("post.html",
                    account=self.account,
                    author=self.author,
                    entry=entry,
                    comments=comments,
                    get_new_comment=get_new_comment,
                    new_comment_error=error)

    def get(self):
        post_id = self.request.get("id")
        action = self.request.get("action")

	# Have to be logged in to do anything comment related.
        if self.logged_in():
            if action == "new":
                self.render_main(post_id, get_new_comment=True)
            elif action == "save":
                self.save_comment(post_id)
            else:
                pass
        else:
            self.render_main(post_id,
                             error="You must be logged in to comment.")

    def save_comment(self, post_id):
        author = self.request.get("author")
        comment_content = self.request.get("comment-content").strip()

        if comment_content:
            record = datastore.Comment.create(
                post_id=post_id,
                author=author,
                commenter=self.account,
                content=comment_content)
            time.sleep(0.1) # for now
            self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
        else:
            self.render_main(post_id,
                              error="Non-empty comment, please!")


class UpdateCommentHandler(BaseHandler):
    """Handler for editing existing comments."""

    def render_main(self, post_id, target="", error=""):
        entry = datastore.BlogEntry.dict_by_id(int(post_id))
        comments = datastore.Comment.by_postid_dict(post_id)

        self.render("post.html",
                    account=self.account,
                    author=self.author,
                    entry=entry,
                    comments=comments,
                    target=target,
                    update_comment_error=error)

    def get(self):
        # Have to be logged in to do anything comment related.
        if self.logged_in():
            self.update_comment()
        else:
            post_id = self.request.get("id")
            self.render_main(post_id,
                             error="You must be logged in to comment.")

    def update_comment(self):
        author = self.request.get("author")
        post_id = self.request.get("id")
        action = self.requst.get("action")

        comment_id = self.request.get("comment_id")
        comment = datastore.Comment.by_id(int(comment_id))
        commenter = comment.commenter

        if commenter == self.account:
            if action == "Edit":
                self.render_main(post_id, target=comment_id)

            elif action == "Delete":
                # Delete from Comment datastore.
                datastore.Comment.delete_by_id(int(comment_id))
                time.sleep(0.1) # for now
                self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))

            elif action == "Save":
                new_content = self.request.get("comment-content").strip()
                if new_content:
                    datastore.Comment.update(int(comment_id), new_content)
                    time.sleep(0.1) # for now
                    self.redirect("/blog/post?author=%s&id=%s" %
                                 (author, post_id))
                else:
                    self.render_main(post_id=post_id,
                                     target=comment_id,
                                     error="Non-empty comment, please!")
            else:
                pass

        else:
            self.render_main(
                post_id,
                target=comment_id,
                error="You can only make changes to your own comments.")


class RateHandler(BaseHandler):
    """Handler for the Like and Dislike buttons.

       Rating feature currently only works if JavaScript is enabled.
    """

    def post(self):
        data = self.request.get("rating")
        if data:
            tmp = data.split("-")
            rating = tmp[0]
            post_id = tmp[1]
            entry = datastore.BlogEntry.by_id(int(post_id))

            if not entry:
                return

            # User must be logged in, and they can't be the author of the post.
            if self.logged_in():
                if self.account != entry.author:
                    # Check to see if this user has already rated it.
                    record = datastore.UserRating.by_username_and_postid(
                        username=self.account,
                        post_id=post_id)

                    if record:
                        # The user has already rated this post, so do nothing.
                        return
                    else:
                        if rating == "like":
                            new_count = datastore.BlogEntry.increment_like(
                                int(post_id))
                        elif rating == "dislike":
                            new_count = datastore.BlogEntry.increment_dislike(
                                int(post_id))

                        datastore.UserRating.create(
                            username=self.account,
                            post_id=post_id,
                            post_author=entry.author,
                            rating=rating)
                        array = {"stat": "ok", "count": str(new_count)}

                else:
                    array = {"stat": "rate_your_own"}

            else:
                array = {"stat": "not_logged_in"}

            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(json.dumps(array))


app = webapp2.WSGIApplication([("/", MainHandler),
                               ("/signup", SignupHandler),
                               ("/login", LoginHandler),
                               ("/logout", LogoutHandler),
                               ("/welcome", WelcomeHandler),
                               ("/blog", BlogHandler),
                               ("/blog/post", PostHandler),
                               ("/blog/new", NewPostHandler),
                               ("/blog/edit", EditHandler),
                               ("/blog/delete", DeleteHandler),
                               ("/blog/newcomment", NewCommentHandler),
                               ("/blog/updatecomment", UpdateCommentHandler),
                               ("/blog/rate", RateHandler)
                               ],
                               debug=True)
