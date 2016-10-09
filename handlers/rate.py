
""" Module classes:
RateHandler - Handler for the Like and Dislike buttons.
"""

import json

from base import BaseHandler
from models.post import BlogEntry
from models.rating import Rating
from models.comment import Comment

##############################################################################

class RateHandler(BaseHandler):
    """Handler for the Like and Dislike buttons."""

    def render_main(self, post_id, author, error=""):
        entry = BlogEntry.dict_by_id(int(post_id))
        comments = Comment.by_postid_dict(post_id)

        entry = BlogEntry.add_ratings(entries = [entry],
                                      username = self.account)[0]

        self.render("post.html",
                    account=self.account,
                    author=author,
                    entry=entry,
                    comments=comments,
                    rating_error=error)
                    
    def get(self, post_id, rating):
        if not self.logged_in():
            self.redirect("/login")
            return
    
        # User must be logged in, they can't be the author of the post,
        # and they can't have already rated it.
        author = BlogEntry.by_id(int(post_id)).author        
        if self.account != author:
            record = Rating.by_username_and_postid(
                username=self.account,
                post_id=post_id)

            if record:
                # This is currently taken care of in post.html, which 
                # only shows a link if you haven't already rated the post.
                
                # The user has already rated this post, so do nothing.
                return
            else:
                if rating == "like":
                    new_count = BlogEntry.increment_like(int(post_id))
                elif rating == "dislike":
                    new_count = BlogEntry.increment_dislike(int(post_id))

                Rating.create(username=self.account,
                              post_id=post_id,
                              post_author=author,
                              rating=rating)
                self.render_main(post_id, author)
        
                # array = {"count": str(new_count)}
        
        else:
            self.render_main(post_id, author, "You can't rate your own post!")
            #array = {"stat": "rate_your_own"}

            # self.response.headers["Content-Type"] = "application/json"
            # self.response.out.write(json.dumps(array))
            