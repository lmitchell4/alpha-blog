
""" Module classes:
EditPostHandler - Handler for editing an existing blog post.
"""

from base import BaseHandler
from models.post import BlogEntry
from models.comment import Comment

##############################################################################

class EditPostHandler(BaseHandler):
    """Handler for editing an existing blog post."""

    def render_error(self, post_id, author, error):
        entry = BlogEntry.dict_by_id(int(post_id))
        entry = BlogEntry.add_ratings(entries = [entry],
                                      username = self.account)[0]
        comments = Comment.by_postid_dict(post_id)

        self.render("post.html",
                    account=self.account,
                    author=author,
                    entry=entry,
                    comments=comments,
                    post_error=error)

    def render_main(self, post_id, error=""):
        entry = BlogEntry.dict_by_id(int(post_id))
        self.render("editpost.html",
                    account=self.account,
                    author=self.account,
                    entry=entry,
                    error=error)

    def get(self, post_id):
        if not self.logged_in():
            self.redirect("/login")
            return

        author = BlogEntry.by_id(int(post_id)).author
        if self.user_and_author(author):
            self.render_main(post_id)
        else:
            self.render_error(post_id, author,
                              error="You can only edit your own posts.")

    def post(self, post_id):
        if not self.logged_in():
            self.redirect("/login")
            return

        author = BlogEntry.by_id(int(post_id)).author
        if self.user_and_author(author):
            new_subject = self.request.get("subject").strip()
            new_content = self.request.get("content").strip()

            if new_subject and new_content:
                BlogEntry.update_by_id(int(post_id), new_subject, new_content)
                self.redirect("/post/%s" % str(post_id))
            else:
                self.render_main(post_id,
                                 error="Non-empty comment, please!")

        else:
            self.redirect("error_404.html")
