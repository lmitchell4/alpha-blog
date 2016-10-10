
""" Module classes:
PostHandler - Handler for the web page for an individual blog post.
"""

from base import BaseHandler

from models.post import BlogEntry
from models.comment import Comment

##############################################################################

class PostHandler(BaseHandler):
    """Handler for the web page for an individual blog post.

       This must handle blog post editing/deleting, commenting,
       and rating capabilities.

    """

    def render_main(self, post_id, author):
        entry = BlogEntry.dict_by_id(int(post_id))
        entry = BlogEntry.add_ratings(entries = [entry],
                                      username = self.account)[0]
        comments = Comment.by_postid_dict(post_id)

        self.render("post.html",
                    account=self.account,
                    author=author,
                    entry=entry,
                    comments=comments)

    def get(self, post_id):
        author = BlogEntry.by_id(int(post_id)).author
        self.render_main(post_id, author)
