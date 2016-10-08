
""" Module classes:
EditPostHandler - Handler for editing an existing blog post.
"""

from base import BaseHandler

from models.post import BlogEntry

##############################################################################

class EditPostHandler(BaseHandler):
    """Handler for editing an existing blog post."""

    def render_main(self, post_id, error=""):
        entry = BlogEntry.dict_by_id(int(post_id))
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
                BlogEntry.update_by_id(
                    int(post_id),
                    new_subject, new_content)
                self.redirect("/blog/post?author=%s&id=%s" %
                              (self.author, post_id))

            else:
                self.render_main(post_id,
                                  error="Non-empty comment, please!")

        elif action == "Cancel":
            self.redirect("/blog?author=%s" % self.account)
