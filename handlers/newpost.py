
""" Module classes:
NewPostHandler - Handler for creating a new blog post.
"""

from base import BaseHandler

from models.post import BlogEntry

##############################################################################

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
                new_entry = BlogEntry.create(
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
