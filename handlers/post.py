
""" Module classes:
PostHandler - Handler for the web page for an individual blog post.
"""

from base import BaseHandler

from models.post import BlogEntry
from models.comment import Comment

##############################################################################

class PostHandler(BaseHandler):
    """Handler for the web page for an individual blog post.

       This must handle blog post editing/deleting, commenting,
       and rating capabilities.

    """

    def render_main(self, post_id, post_error="", get_new_comment = False,
                    new_comment_error="", update_target="",
                    update_comment_error=""):
        entry = BlogEntry.dict_by_id(int(post_id))
        comments = Comment.by_postid_dict(post_id)

        entry = BlogEntry.add_ratings(entries = [entry],
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
            comment = Comment.by_id(int(comment_id))

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
            record = Comment.create(
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
            Comment.delete_by_id(int(comment_id))
            time.sleep(0.1) # for now
            self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))

        elif action == "Save":
            new_content = self.request.get("comment-content").strip()
            if new_content:
                Comment.update(int(comment_id), new_content)
                time.sleep(0.1) # for now
                self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
            else:
                self.render_main(
                    post_id=post_id,
                    update_target=comment_id,
                    update_comment_error="Comments can't be empty!")

        elif action == "Cancel":
            self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
