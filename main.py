
""" Module classes:
BaseHandler - Handler for rendering templates and manipulating Cookies.

SignupHandler - Handler for the signup page.
LoginHandler - Handler for the login page.
LogoutHandler - Handler for logging out.

MainHandler - Handler for the web site home page.
UserHomeHandler - Handler for a user's home page.
NewPostHandler - Handler for creating a new blog post.
PostHandler - Handler for the web page for an individual blog post.
EditPostHandler - Handler for editing an existing blog post.
DeletePostHandler - Handler for deleting an existing blog post.
NewCommentHandler - Handler for new comments.
UpdateCommentHandler - Handler for editing existing comments.
RateHandler - Handler for the Like and Dislike buttons.

This project is based on code developed by Udacity.
"""

# import os
# import json
# import time

import webapp2
# import jinja2

# # from base import BaseHandler

from index import MainHandler
from signup import SignupHandler
from login import LoginHandler
from logout import LogoutHandler
from userhome import UserHomeHandler
from post import PostHandler
from newpost import NewPostHandler
from editpost import EditPostHandler
from deletepost import  DeletePostHandler
from newcomment import  NewCommentHandler
from updatecomment import UpdateCommentHandler
from rate import RateHandler

# import models
# import validate

# import handlers
# import validate

# from user import UserAccount
# from post import BlogEntry
# from comment import Comment
# from rating import Rating

##############################################################################

app = webapp2.WSGIApplication([("/", MainHandler),
                               ("/signup", SignupHandler),
                               ("/login", LoginHandler),
                               ("/logout", LogoutHandler),
                               ("/blog", UserHomeHandler),
                               ("/blog/post", PostHandler),
                               ("/blog/new", NewPostHandler),
                               ("/blog/edit", EditPostHandler),
                               ("/blog/delete", DeletePostHandler),
                               ("/blog/newcomment", NewCommentHandler),
                               ("/blog/updatecomment", UpdateCommentHandler),
                               ("/blog/rate", RateHandler)
                               ],
                               debug=True)



## Blog Handlers:

# # class MainHandler(BaseHandler):
    # # """Handler for the web site home page."""

    # # def get(self):
        # # all_users = UserAccount.get_all_usernames()
        # # if all_users:
            # # self.render("index.html",
                        # # account=self.account,
                        # # usernames=all_users)
        # # else:
            # # self.render("index.html",
                        # # account=self.account)


# # class UserHomeHandler(BaseHandler):
    # # """Handler for a user's home page.

       # # Currently not handling the Search button on this page.

    # # """

    # # def render_main(self, error_msg=""):
        # # blog_entries = BlogEntry.first_ten_list(self.author)

        # # # Get all rating information for this user and author:
        # # if blog_entries and self.logged_in():
            # # blog_entries = BlogEntry.add_ratings(
                # # entries=blog_entries,
                # # username=self.account)

        # # self.render("blog.html",
            # # account=self.account,
            # # author=self.author,
            # # blog_entries=blog_entries,
            # # error_msg=error_msg)

    # # def get(self):
        # # self.render_main()

    # # def post(self):
        # # action = self.request.get("newpost")
        # # if action == "New Post" and self.user_and_author():
            # # self.redirect("/blog/new")
        # # else:
            # # self.render_main("You must be logged in to your account " +
                             # # "to create a new blog post.")


# # class NewPostHandler(BaseHandler):
    # # """Handler for creating a new blog post."""

    # # def render_main(self, subject="", content="", error=""):
        # # self.render("newpost.html",
                    # # account=self.account,
                    # # author=self.account,
                    # # subject=subject,
                    # # content=content,
                    # # error=error)

    # # def get(self):
        # # self.render_main()

    # # def post(self):
        # # action = self.request.get("newpost-opt")

        # # if action == "Create":
            # # subject = self.request.get("subject").strip()
            # # content = self.request.get("content").strip()

            # # if subject and content:
                # # new_entry = BlogEntry.create(
                    # # author=self.account,
                    # # subject=subject,
                    # # content=content)
                # # self.redirect("/blog/post?author=%s&id=%s" %
                              # # (self.account, str(new_entry.key.id())))

            # # else:
                # # error = "Subject and content, please!"
                # # self.render_new(subject, content, error)

        # # elif action == "Cancel":
            # # self.redirect("/blog?author=%s" % self.account)


# # class PostHandler(BaseHandler):
    # # """Handler for the web page for an individual blog post.

       # # This must handle blog post editing/deleting, commenting,
       # # and rating capabilities.

    # # """

    # # def render_main(self, post_id, post_error="", get_new_comment = False,
                    # # new_comment_error="", update_target="",
                    # # update_comment_error=""):
        # # entry = BlogEntry.dict_by_id(int(post_id))
        # # comments = Comment.by_postid_dict(post_id)

        # # entry = BlogEntry.add_ratings(entries = [entry],
                                                 # # username = self.account)
        # # entry = entry[0]

        # # self.render("post.html",
                    # # account=self.account,
                    # # author=self.author,
                    # # entry=entry,
                    # # comments=comments,
                    # # post_error=post_error,
                    # # get_new_comment=get_new_comment,
                    # # new_comment_error=new_comment_error,
                    # # update_target=update_target,
                    # # update_comment_error=update_comment_error)

    # # def get(self):
        # # post_id = self.request.get("id")
        # # self.render_main(post_id=post_id)

    # # def post(self):
        # # author = self.request.get("author")
        # # post_id = self.request.get("id")

        # # # If the action is related to the post:
        # # action = self.request.get("changepost")
        # # if action:
            # # action = action.lower()
            # # if self.user_and_author():
                # # self.redirect("/blog/%s?author=%s&id=%s" %
                              # # (action, author, post_id))
            # # else:
                # # self.render_main(
                    # # post_id=post_id,
                    # # post_error="You can only %s your own posts." % action)
            # # return

        # # # If the action is related to a new comment:
        # # action = self.request.get("newcomment")
        # # if action:
            # # if self.logged_in():
                # # if action == "Add Comment":
                    # # self.render_main(post_id, get_new_comment=True)
                # # elif action == "Save":
                    # # self.save_comment(post_id, author)
                # # elif action == "Cancel":
                    # # self.redirect("/blog/post?author=%s&id=%s" %
                                  # # (author, post_id))

            # # else:
                # # self.render_main(
                    # # post_id,
                    # # get_new_comment=False,
                    # # new_comment_error="You must be logged in to comment.")
            # # return

        # # # If the action is related to an existing comment:
        # # action = self.request.get("updatecomment")
        # # if action:
            # # comment_id = self.request.get("comment_id")
            # # comment = Comment.by_id(int(comment_id))

            # # if comment.commenter == self.account:
                # # self.update_comment(post_id, author, comment_id, action)
            # # else:
                # # self.render_main(
                    # # post_id,
                    # # update_target=comment_id,
                    # # update_comment_error=
                        # # "You can only make changes to your own comments.")

    # # def save_comment(self, post_id, author):
        # # comment_content = self.request.get("comment-content").strip()

        # # if comment_content:
            # # # use author from the get parameters or from self.author?
            # # record = Comment.create(
                # # post_id=post_id,
                # # author=author,
                # # commenter=self.account,
                # # content=comment_content)
            # # time.sleep(0.1) # for now
            # # self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
        # # else:
            # # self.render_main(
                # # post_id,
                # # get_new_comment=True,
                # # new_comment_error="Comments can't be empty!")

    # # def update_comment(self, post_id, author, comment_id, action):
        # # if action == "Edit":
            # # self.render_main(post_id, update_target=comment_id)

        # # elif action == "Delete":
            # # # Delete from Comment datastore.
            # # Comment.delete_by_id(int(comment_id))
            # # time.sleep(0.1) # for now
            # # self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))

        # # elif action == "Save":
            # # new_content = self.request.get("comment-content").strip()
            # # if new_content:
                # # Comment.update(int(comment_id), new_content)
                # # time.sleep(0.1) # for now
                # # self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
            # # else:
                # # self.render_main(
                    # # post_id=post_id,
                    # # update_target=comment_id,
                    # # update_comment_error="Comments can't be empty!")

        # # elif action == "Cancel":
            # # self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))


# # class EditPostHandler(BaseHandler):
    # # """Handler for editing an existing blog post."""

    # # def render_main(self, post_id, error=""):
        # # entry = BlogEntry.dict_by_id(int(post_id))
        # # self.render("editpost.html",
                    # # account=self.account,
                    # # author=self.account,
                    # # entry=entry,
                    # # error=error)

    # # def get(self):
        # # post_id = self.request.get("id")
        # # self.render_main(post_id=post_id)

    # # def post(self):
        # # action = self.request.get("editpost-opt")

        # # if action == "Save":
            # # new_subject = self.request.get("subject")
            # # new_content = self.request.get("content").strip()

            # # if new_content:
                # # post_id = self.request.get("id")
                # # BlogEntry.update_by_id(
                    # # int(post_id),
                    # # new_subject, new_content)
                # # self.redirect("/blog/post?author=%s&id=%s" %
                              # # (self.author, post_id))

            # # else:
                # # self.render_main(post_id,
                                  # # error="Non-empty comment, please!")

        # # elif action == "Cancel":
            # # self.redirect("/blog?author=%s" % self.account)


# # class DeletePostHandler(BaseHandler):
    # # """Handler for deleting an existing blog post.

       # # There is currently no option to undo a deletion.

    # # """
    # # def render_main(self, post_subject):
        # # self.render("delete.html",
                    # # account=self.account,
                    # # author=self.author,
                    # # post_subject=post_subject)

    # # def get(self):
        # # # Make sure the author is the one logged in.
        # # if self.user_and_author():
            # # # Delete the post and any associated comments.
            # # post_id = self.request.get("id")
            # # blog_entry = BlogEntry.get_by_id(int(post_id))
            # # post_subject = blog_entry.subject

            # # BlogEntry.delete_by_id(int(post_id))
            # # Comment.delete_all_by_postid(post_id)

            # # self.render_main(post_subject = post_subject)


# # class NewCommentHandler(BaseHandler):
    # # """Handler for new comments."""

    # # def render_main(self, post_id, get_new_comment=False, error=""):
        # # entry = BlogEntry.dict_by_id(int(post_id))
        # # comments = Comment.by_postid_dict(post_id)

        # # self.render("post.html",
                    # # account=self.account,
                    # # author=self.author,
                    # # entry=entry,
                    # # comments=comments,
                    # # get_new_comment=get_new_comment,
                    # # new_comment_error=error)

    # # def get(self):
        # # post_id = self.request.get("id")
        # # action = self.request.get("action")

	# # # Have to be logged in to do anything comment related.
        # # if self.logged_in():
            # # if action == "new":
                # # self.render_main(post_id, get_new_comment=True)
            # # elif action == "save":
                # # self.save_comment(post_id)
            # # else:
                # # pass
        # # else:
            # # self.render_main(post_id,
                             # # error="You must be logged in to comment.")

    # # def save_comment(self, post_id):
        # # author = self.request.get("author")
        # # comment_content = self.request.get("comment-content").strip()

        # # if comment_content:
            # # record = Comment.create(
                # # post_id=post_id,
                # # author=author,
                # # commenter=self.account,
                # # content=comment_content)
            # # time.sleep(0.1) # for now
            # # self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
        # # else:
            # # self.render_main(post_id,
                              # # error="Non-empty comment, please!")


# # class UpdateCommentHandler(BaseHandler):
    # # """Handler for editing existing comments."""

    # # def render_main(self, post_id, target="", error=""):
        # # entry = BlogEntry.dict_by_id(int(post_id))
        # # comments = Comment.by_postid_dict(post_id)

        # # self.render("post.html",
                    # # account=self.account,
                    # # author=self.author,
                    # # entry=entry,
                    # # comments=comments,
                    # # target=target,
                    # # update_comment_error=error)

    # # def get(self):
        # # # Have to be logged in to do anything comment related.
        # # if self.logged_in():
            # # self.update_comment()
        # # else:
            # # post_id = self.request.get("id")
            # # self.render_main(post_id,
                             # # error="You must be logged in to comment.")

    # # def update_comment(self):
        # # author = self.request.get("author")
        # # post_id = self.request.get("id")
        # # action = self.requst.get("action")

        # # comment_id = self.request.get("comment_id")
        # # comment = Comment.by_id(int(comment_id))
        # # commenter = comment.commenter

        # # if commenter == self.account:
            # # if action == "Edit":
                # # self.render_main(post_id, target=comment_id)

            # # elif action == "Delete":
                # # # Delete from Comment datastore.
                # # Comment.delete_by_id(int(comment_id))
                # # time.sleep(0.1) # for now
                # # self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))

            # # elif action == "Save":
                # # new_content = self.request.get("comment-content").strip()
                # # if new_content:
                    # # Comment.update(int(comment_id), new_content)
                    # # time.sleep(0.1) # for now
                    # # self.redirect("/blog/post?author=%s&id=%s" %
                                 # # (author, post_id))
                # # else:
                    # # self.render_main(post_id=post_id,
                                     # # target=comment_id,
                                     # # error="Non-empty comment, please!")
            # # else:
                # # pass

        # # else:
            # # self.render_main(
                # # post_id,
                # # target=comment_id,
                # # error="You can only make changes to your own comments.")


# # class RateHandler(BaseHandler):
    # # """Handler for the Like and Dislike buttons.

       # # Rating feature currently only works if JavaScript is enabled.
    # # """

    # # def post(self):
        # # data = self.request.get("rating")
        # # if data:
            # # tmp = data.split("-")
            # # rating = tmp[0]
            # # post_id = tmp[1]
            # # entry = BlogEntry.by_id(int(post_id))

            # # if not entry:
                # # return

            # # # User must be logged in, and they can't be the author of the post.
            # # if self.logged_in():
                # # if self.account != entry.author:
                    # # # Check to see if this user has already rated it.
                    # # record = Rating.by_username_and_postid(
                        # # username=self.account,
                        # # post_id=post_id)

                    # # if record:
                        # # # The user has already rated this post, so do nothing.
                        # # return
                    # # else:
                        # # if rating == "like":
                            # # new_count = BlogEntry.increment_like(
                                # # int(post_id))
                        # # elif rating == "dislike":
                            # # new_count = BlogEntry.increment_dislike(
                                # # int(post_id))

                        # # Rating.create(
                            # # username=self.account,
                            # # post_id=post_id,
                            # # post_author=entry.author,
                            # # rating=rating)
                        # # array = {"stat": "ok", "count": str(new_count)}

                # # else:
                    # # array = {"stat": "rate_your_own"}

            # # else:
                # # array = {"stat": "not_logged_in"}

            # # self.response.headers["Content-Type"] = "application/json"
            # # self.response.out.write(json.dumps(array))



