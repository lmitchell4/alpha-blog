
""" Module classes:
NewPostHandler - Handler for creating a new blog post.
"""

from base import BaseHandler

from models.post import BlogEntry

##############################################################################

class NewPostHandler(BaseHandler):
    """Handler for creating a new blog post."""

    def render_error(self, author, error=""):
        blog_entries = BlogEntry.first_ten_list(author)

        # Get all rating information for this user and author:
        if blog_entries and self.logged_in():
            blog_entries = BlogEntry.add_ratings(entries=blog_entries,
                                                 username=self.account)

        self.render("home.html",
            account=self.account,
            author=author,
            blog_entries=blog_entries,
            error_msg=error)

    def render_main(self, author, subject="", content="", error=""):
        self.render("newpost.html",
                    account=self.account,
                    author=author,
                    subject=subject,
                    content=content,
                    error=error)

    def get(self, author):
        if not self.logged_in():
            self.redirect("/login")
            return

        if self.user_and_author(author):
            self.render_main(author)
        else:
            self.render_error(
                author,
                error="You can only create posts on your own blog.")

    def post(self, author):
        if not self.logged_in():
            self.redirect("/login")
            return

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

        else:
            self.redirect("error_404.html")
