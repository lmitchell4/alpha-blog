
""" Module classes:
DeletePostHandler - Handler for deleting an existing blog post.
"""

from base import BaseHandler
from models.post import BlogEntry
from models.comment import Comment

##############################################################################

class DeletePostHandler(BaseHandler):
    """Handler for deleting an existing blog post.

       There is currently no option to undo a deletion.

    """
    def render_main(self, post_subject):
        self.render("delete.html",
                    account=self.account,
                    author=self.author,
                    post_subject=post_subject)

    def get(self):
        # Make sure the author is the one logged in.
        if self.user_and_author():
            # Delete the post and any associated comments.
            post_id = self.request.get("id")
            blog_entry = BlogEntry.get_by_id(int(post_id))
            post_subject = blog_entry.subject

            BlogEntry.delete_by_id(int(post_id))
            Comment.delete_all_by_postid(post_id)

            self.render_main(post_subject = post_subject)
