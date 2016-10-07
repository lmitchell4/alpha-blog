
""" Module summary:
Constants and functions for hashing passwords and validating
user account information.
"""

import re
import random
import string
import hmac

###############################################################################


SECRET = 'dj8264mdu0a6d10d8ak'


##########################################
## Password hashing functions:

def make_salt():
    """For generating a five letter salt string."""
    return "".join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    """For constructing a hashed password using salt and hmac.

       Returns the hashed value in this format:
           HASH(name + pw + salt)|salt
    """
    if not salt:
        salt = make_salt()
    h = hmac.new("", name + pw + salt).hexdigest()

    return "%s|%s" % (h, salt)

def valid_pw(name, pw, h):
    """For verifying that a submitted password is correct by
       checking it against the hashed password saved in a database.

       h should be a hashed password in the format: HASH(name + pw + salt),salt.
       Given the username, submitted password, and the salt value from h,
       construct the hashed password and check that it matches the saved
       value.
    """
    salt = h.split("|")[1]
    check_hash = make_pw_hash(name, pw, salt)
    return check_hash == h


##########################################
## Cookie hashing functions:

def make_secure_val(s):
    """For constructing a hashed version of the string s.

       Use this function to construct cookies that can be used
       to verify that a user is logged in.

       Returns the hashed value in this format:
           s|HASH(s)
    """
    hash_str = hmac.new(SECRET, s).hexdigest()
    return "%s|%s" % (s, hash_str)

def check_secure_val(h):
    """For verifying that a string of the form val|HASH(val) is
       valid, where val is a string and HASH(val) is the hashed version
       of val.

       This is for checking cookies that represent a logged in user.
    """
    val = h.split("|")[0]
    if h == make_secure_val(val):
        return val
    else:
        return None


##########################################
## User data verification functions:

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USERNAME_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)
