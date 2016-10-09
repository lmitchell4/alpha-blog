
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

    def render_main(self, author, error_msg=""):
        # blog_entries = BlogEntry.first_ten_list(self.author)
        blog_entries = BlogEntry.first_ten_list(author)

        # Get all rating information for this user and author:
        if blog_entries and self.logged_in():
            blog_entries = BlogEntry.add_ratings(
                entries=blog_entries,
                username=self.account)

        self.render("home.html",
            account=self.account,
            # author=self.author,
            author=author,
            blog_entries=blog_entries,
            error_msg=error_msg)

    # def get(self, author):
        # self.render_main(author)

    def get(self, author):
        # # author = self.request.path.split("/")[2]
        self.render_main(author)
    
    # def post(self):
        # action = self.request.get("newpost")
        # if action == "New Post" and self.user_and_author():
            # self.redirect("/new")
        # else:
            # self.render_main("You must be logged in to your account " +
                             # "to create a new blog post.")
