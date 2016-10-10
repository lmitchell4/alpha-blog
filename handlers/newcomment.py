
""" Module classes:
NewCommentHandler - Handler for new comments.
"""

import time

from base import BaseHandler
from models.post import BlogEntry
from models.comment import Comment

##############################################################################

class NewCommentHandler(BaseHandler):
    """Handler for new comments."""

    def render_main(self, post_id, entry, get_new_comment=False, error=""):
        entry = BlogEntry.add_ratings(entries = [entry],
                                      username = self.account)[0]
        comments = Comment.by_postid_dict(post_id)

        self.render("post.html",
                    account=self.account,
                    author=entry["author"],
                    entry=entry,
                    comments=comments,
                    get_new_comment=get_new_comment,
                    new_comment_error=error)

    def get(self, post_id):
        if not self.logged_in():
            self.redirect("/login")
            return

        entry = BlogEntry.dict_by_id(int(post_id))
        self.render_main(post_id, entry=entry, get_new_comment=True)

    def post(self, post_id):
        if not self.logged_in():
            self.redirect("/login")
            return

        entry = BlogEntry.dict_by_id(int(post_id))
        comment_content = self.request.get("comment-content").strip()
        if comment_content:
            record = Comment.create(post_id=post_id,
                                    author=entry["author"],
                                    commenter=self.account,
                                    content=comment_content)
            time.sleep(0.1) # for now
            self.redirect("/post/%s" % post_id)
        else:
            self.render_main(post_id=post_id,
                             entry=entry,
                             get_new_comment=False,
                             error="Non-empty comments only!")
