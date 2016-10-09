
""" Module classes:
This project is based on code developed by Udacity.
"""

import webapp2

from index import MainHandler
from signup import SignupHandler
from login import LoginHandler
from logout import LogoutHandler
from home import UserHomeHandler
from post import PostHandler
from newpost import NewPostHandler
from editpost import EditPostHandler
from deletepost import  DeletePostHandler
from newcomment import  NewCommentHandler
from editcomment import EditCommentHandler
from deletecomment import DeleteCommentHandler
from rate import RateHandler

##############################################################################

app = webapp2.WSGIApplication(
    [("/", MainHandler),
     ("/signup", SignupHandler),
     ("/login", LoginHandler),
     ("/logout", LogoutHandler),
     ("/home/([a-zA-z]+)", UserHomeHandler), 
     ("/post/([0-9]+)", PostHandler),
     ("/new/([a-zA-z]+)", NewPostHandler),
     ("/edit/([0-9]+)", EditPostHandler),
     ("/delete/([0-9]+)", DeletePostHandler),
     ("/newcomment/([0-9]+)", NewCommentHandler),
     ("/editcomment/([0-9]+)", EditCommentHandler),
     ("/deletecomment/([0-9]+)", DeleteCommentHandler),
     ("/rate", RateHandler)
    ], debug=True)


# if not logged in, redirect to signup page
# import time not being handled very cleanly