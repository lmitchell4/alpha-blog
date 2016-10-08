
""" Module classes:
UpdateCommentHandler - Handler for editing existing comments.
"""

from base import BaseHandler

from models.post import BlogEntry
from models.comment import Comment

##############################################################################

class UpdateCommentHandler(BaseHandler):
    """Handler for editing existing comments."""

    def render_main(self, post_id, target="", error=""):
        entry = BlogEntry.dict_by_id(int(post_id))
        comments = Comment.by_postid_dict(post_id)

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
        comment = Comment.by_id(int(comment_id))
        commenter = comment.commenter

        if commenter == self.account:
            if action == "Edit":
                self.render_main(post_id, target=comment_id)

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
