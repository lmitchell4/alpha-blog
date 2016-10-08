
""" Module classes:
NewCommentHandler - Handler for new comments.
"""

from base import BaseHandler

from models.post import BlogEntry
from models.comment import Comment

##############################################################################

class NewCommentHandler(BaseHandler):
    """Handler for new comments."""

    def render_main(self, post_id, get_new_comment=False, error=""):
        entry = BlogEntry.dict_by_id(int(post_id))
        comments = Comment.by_postid_dict(post_id)

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
            record = Comment.create(
                post_id=post_id,
                author=author,
                commenter=self.account,
                content=comment_content)
            time.sleep(0.1) # for now
            self.redirect("/blog/post?author=%s&id=%s" % (author, post_id))
        else:
            self.render_main(post_id,
                              error="Non-empty comment, please!")
