
""" Module classes:
This project is based on code developed by Udacity.
"""

import webapp2

from index import MainHandler
from signup import SignupHandler
from login import LoginHandler
from logout import LogoutHandler
from userhome import UserHomeHandler
from post import PostHandler
from newpost import NewPostHandler
from editpost import EditPostHandler
from deletepost import  DeletePostHandler
from newcomment import  NewCommentHandler
from updatecomment import UpdateCommentHandler
from rate import RateHandler

##############################################################################

app = webapp2.WSGIApplication([("/", MainHandler),
                               ("/signup", SignupHandler),
                               ("/login", LoginHandler),
                               ("/logout", LogoutHandler),
                               ("/blog", UserHomeHandler),
                               ("/blog/post", PostHandler),
                               ("/blog/new", NewPostHandler),
                               ("/blog/edit", EditPostHandler),
                               ("/blog/delete", DeletePostHandler),
                               ("/blog/newcomment", NewCommentHandler),
                               ("/blog/updatecomment", UpdateCommentHandler),
                               ("/blog/rate", RateHandler)
                               ],
                               debug=True)
