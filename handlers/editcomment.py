
""" Module classes:
EditCommentHandler - Handler for editing existing comments.
"""

import time

from base import BaseHandler
from models.post import BlogEntry
from models.comment import Comment

##############################################################################

class EditCommentHandler(BaseHandler):
    """Handler for editing existing comments."""

    def render_main(self, post_id, target="", error=""):
        entry = BlogEntry.dict_by_id(int(post_id))
        entry = BlogEntry.add_ratings(entries = [entry],
                                      username = self.account)[0]
        comments = Comment.by_postid_dict(post_id)

        self.render("post.html",
                    account=self.account,
                    author=entry["author"],
                    entry=entry,
                    comments=comments,
                    edit_comment_target=target,
                    edit_comment_error=error)

    def get(self, comment_id):
        comment = Comment.by_id(int(comment_id))
        commenter = comment.commenter
        post_id = comment.post_id

        if not self.logged_in():
            self.render_main(
                post_id,
                target=comment_id,
                error="You must be logged in to comment.")
            return

        if self.account == commenter:
            self.render_main(post_id, target=comment_id)
        else:
            self.render_main(
                post_id,
                target=comment_id,
                error="You can only edit your own comments.")

    def post(self, comment_id):
        comment = Comment.by_id(int(comment_id))
        commenter = comment.commenter
        post_id = comment.post_id

        if self.logged_in() and self.account == commenter:
            new_content = self.request.get("comment-content").strip()

            if new_content:
                Comment.update(int(comment_id), new_content)
                time.sleep(0.1) # for now
                self.redirect("/post/%s" % post_id)
            else:
                self.render_main(
                    post_id,
                    target=comment_id,
                    error="Non-empty comments only!")

        else:
            self.redirect("error_404.html")
