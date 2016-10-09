
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

    def render_main(self, post_id, author,
                    get_new_comment = False,
                    new_comment_error="", 
                    update_target="",
                    edit_comment_error=""):
        entry = BlogEntry.dict_by_id(int(post_id))
        comments = Comment.by_postid_dict(post_id)

        entry = BlogEntry.add_ratings(entries = [entry],
                                      username = self.account)[0]

        self.render("post.html",
                    account=self.account,
                    author=author,
                    entry=entry,
                    comments=comments,
                    get_new_comment=get_new_comment,
                    new_comment_error=new_comment_error,
                    update_target=update_target,
                    edit_comment_error=edit_comment_error)

    def get(self, post_id):
        author = BlogEntry.by_id(int(post_id)).author
        self.render_main(post_id, author)
