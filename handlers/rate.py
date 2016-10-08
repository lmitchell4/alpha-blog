
""" Module classes:
RateHandler - Handler for the Like and Dislike buttons.
"""

import json

from base import BaseHandler
from models.post import BlogEntry
from models.rating import Rating

##############################################################################

class RateHandler(BaseHandler):
    """Handler for the Like and Dislike buttons.

       Rating feature currently only works if JavaScript is enabled.
    """

    def post(self):
        data = self.request.get("rating")
        if data:
            tmp = data.split("-")
            rating = tmp[0]
            post_id = tmp[1]
            entry = BlogEntry.by_id(int(post_id))

            if not entry:
                return

            # User must be logged in, and they can't be the author of the post.
            if self.logged_in():
                if self.account != entry.author:
                    # Check to see if this user has already rated it.
                    record = Rating.by_username_and_postid(
                        username=self.account,
                        post_id=post_id)

                    if record:
                        # The user has already rated this post, so do nothing.
                        return
                    else:
                        if rating == "like":
                            new_count = BlogEntry.increment_like(
                                int(post_id))
                        elif rating == "dislike":
                            new_count = BlogEntry.increment_dislike(
                                int(post_id))

                        Rating.create(
                            username=self.account,
                            post_id=post_id,
                            post_author=entry.author,
                            rating=rating)
                        array = {"stat": "ok", "count": str(new_count)}

                else:
                    array = {"stat": "rate_your_own"}

            else:
                array = {"stat": "not_logged_in"}

            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(json.dumps(array))
