
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
    def render_main(self, author, subject):
        self.render("delete.html",
                    account=self.account,
                    author=author,
                    subject=subject)

    def get(self, post_id):
        author = BlogEntry.by_id(int(post_id)).author
        
        # Make sure the author is the one logged in.
        if self.user_and_author(author):
            # Delete the post and any associated comments.
            blog_entry = BlogEntry.get_by_id(int(post_id))
            subject = blog_entry.subject

            BlogEntry.delete_by_id(int(post_id))
            Comment.delete_all_by_postid(post_id)

            self.render_main(author, subject)

        # else:
            # # self.response.write(str(post_id))
            # # self.redirect("/post/%s" % str(post_id))
            # self.redirect("/post/%s" % str(post_id))
