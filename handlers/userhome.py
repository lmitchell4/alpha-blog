
""" Module classes:
UserHomeHandler - Handler for a user's home page.
"""

from base import BaseHandler

from models.post import BlogEntry

##############################################################################

class UserHomeHandler(BaseHandler):
    """Handler for a user's home page.

       Currently not handling the Search button on this page.

    """

    def render_main(self, error_msg=""):
        blog_entries = BlogEntry.first_ten_list(self.author)

        # Get all rating information for this user and author:
        if blog_entries and self.logged_in():
            blog_entries = BlogEntry.add_ratings(
                entries=blog_entries,
                username=self.account)

        self.render("blog.html",
            account=self.account,
            author=self.author,
            blog_entries=blog_entries,
            error_msg=error_msg)

    def get(self):
        self.render_main()

    def post(self):
        action = self.request.get("newpost")
        if action == "New Post" and self.user_and_author():
            self.redirect("/blog/new")
        else:
            self.render_main("You must be logged in to your account " +
                             "to create a new blog post.")
