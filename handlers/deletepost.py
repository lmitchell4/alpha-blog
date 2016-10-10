
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

    def render_error(self, post_id, author, error):
        entry = BlogEntry.dict_by_id(int(post_id))
        entry = BlogEntry.add_ratings(entries = [entry],
                                      username = self.account)[0]
        comments = Comment.by_postid_dict(post_id)

        self.render("post.html",
                    account=self.account,
                    author=author,
                    entry=entry,
                    comments=comments,
                    post_error=error)

    def render_main(self, author, subject):
        self.render("delete.html",
                    account=self.account,
                    author=author,
                    subject=subject)

    def get(self, post_id):
        if not self.logged_in():
            self.redirect("/login")
            return

        author = BlogEntry.by_id(int(post_id)).author
        if self.user_and_author(author):
            # Delete the post and any associated comments.
            blog_entry = BlogEntry.get_by_id(int(post_id))
            subject = blog_entry.subject

            BlogEntry.delete_by_id(int(post_id))
            Comment.delete_all_by_postid(post_id)

            self.render_main(author, subject)
        else:
            self.render_error(post_id, author,
                              error="You can only delete your own posts.")
