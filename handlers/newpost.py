
""" Module classes:
NewPostHandler - Handler for creating a new blog post.
"""

from base import BaseHandler

from models.post import BlogEntry

##############################################################################

class NewPostHandler(BaseHandler):
    """Handler for creating a new blog post."""

    def render_main(self, author, subject="", content="", error=""):
        self.render("newpost.html",
                    account=self.account,
                    author=author,
                    subject=subject,
                    content=content,
                    error=error)

    def get(self, author):
        # # author = self.request.path.split("/")[2]
        
        if self.user_and_author(author):
            self.render_main(author)
        else:
            self.render()

    def post(self, author):
        # # author = self.request.path.split("/")[2]
        
        if self.user_and_author(author):
            subject = self.request.get("subject").strip()
            content = self.request.get("content").strip()

            if subject and content:
                new_entry = BlogEntry.create(
                    author=self.account,
                    subject=subject,
                    content=content)
                self.redirect("/post/%s" % str(new_entry.key.id()))

            else:
                error = "Subject and content, please!"
                self.render_main(author, subject, content, error)
