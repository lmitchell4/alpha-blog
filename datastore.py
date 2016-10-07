
""" Module classes:
UserAccount - a datastore for user account information.
UserRating - a datastore for post ratings.
BlogEntry - a datastore for user blog entries, or "posts".
Comment - a datastore for blog comments.

Note that all the datastore inheriting from ndb.Model use the
default key style.
"""

import string

from google.appengine.ext import ndb

import inputcheck

###############################################################################
## Datastores:

class UserAccount(ndb.Model):
    """Datastore for user account information."""

    username = ndb.StringProperty(required = True)
    password_hash = ndb.TextProperty(required = True)
    email = ndb.StringProperty(required = False)
    created = ndb.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)   # # , parent = users_key())

    @classmethod
    def by_username(cls, username):
        user = cls.query(cls.username == username).get()
        return user

    @classmethod
    def create(cls, username, password, email = None):
        """For creating a new user account."""
        password_hash = inputcheck.make_pw_hash(username, password)
        record = cls(username=username,
                     password_hash=password_hash,
                     email=email)
        record.put()
        return record

    @classmethod
    def login(cls, username, password):
        """For validating a username and password, and logging the user in.

           Check that the user existing in the datastore.
           Check that the password is correct.
        """
        user = cls.by_username(username)
        if user and inputcheck.valid_pw(username, password, user.password_hash):
            return user
        else:
            return None

    @classmethod
    def get_all_usernames(cls):
        """For retrieving all usernames and returning them in a list."""

        all_users = cls.query()
        all_users_usernames = [user.username for user in all_users]
        return all_users_usernames

    @classmethod
    def last_ten_usernames(cls):
        """For retrieving the usernames of the last 10 accounts to be
           created.
        """
        last_ten = cls.query().fetch(10)
        last_ten_usernames = [user.username for user in last_ten]
        return last_ten_usernames


class UserRating(ndb.Model):
    """Datastore for post ratings.

       post_id and post_author refer to the post being rated.
       Currently, no option to change/delete ratings.
    """

    username = ndb.StringProperty(required = True)
    post_id = ndb.StringProperty(required = True)
    post_author = ndb.StringProperty(required = True)
    rating = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)   # # , parent = users_key())

    @classmethod
    def by_username_and_postid(cls, username, post_id):
        record = cls.query(cls.username == username,
                           cls.post_id == post_id).get()
        return record

    @classmethod
    def create(cls, username, post_id, post_author, rating):
        """For creating a new user rating."""
        record = cls(username=username,
                     post_id=post_id,
                     post_author=post_author,
                     rating=rating)
        record.put()
        return record

    @classmethod
    def to_list(cls, records):
        """For converting a set of records to a list of dictionaries."""
        if records:
            record_list = [cls.to_dict(record) for record in records]
            return record_list
        else:
            return []


class BlogEntry(ndb.Model):
    """Datastore for user blog entries, or "posts"."""

    author = ndb.StringProperty(required = True)
    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    likes = ndb.IntegerProperty(required = True)
    dislikes = ndb.IntegerProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, id):
        return cls.get_by_id(id)   # # , parent = users_key())

    @classmethod
    def by_author(cls, author):
        user = cls.query(cls.author == author).get()
        return user

    @classmethod
    def to_dict(cls, entry):
        """For converting a given blog entry to a dictionary."""
        entry_dict = {"post_id": str(entry.key.id()),
                      "author": entry.author,
                      "subject": entry.subject,
                      "content": entry.content,
                      "created": entry.created.strftime("%b %d, %Y"),
                      "likes": entry.likes,
                      "dislikes": entry.dislikes
                     }
        return entry_dict

    @classmethod
    def dict_by_id(cls, id):
        """For retrieving a specific blog entry by id and converting
           it to a dictionary.
        """

        entry = cls.by_id(id)
        entry_dict = cls.to_dict(entry)
        return entry_dict

    @classmethod
    def first_ten_list(cls, author):
        """For converting a set of blog entries to a list of
           dictionaries.
        """

        query = cls.query(cls.author == author)
        first_ten = query.order(-cls.created).fetch(10)

        if first_ten:
            first_ten = [cls.to_dict(entry) for entry in first_ten]
            return first_ten
        else:
            return []

    @classmethod
    def add_ratings(cls, entries, username):
        """For checking whether a given user has rated blog entries.

           entries = a list of dictionaries, where each dictionary
                       represents a blog post, e.g., output from
                       BlogEntry.first_ten_list().
           username = an account username. This should be the username
                       of the user currently logged in (when applicable).

           For each post that has been rated by the user, add a
           dictionary value representing the rating.

           Use the appropriate rating, "Like" or "Dislike", as both the
           dictionary key and the value.
        """

        for entry in entries:
            rating_record = UserRating.by_username_and_postid(
                username=username,
                post_id=entry["post_id"])
            if rating_record:
                entry[rating_record.rating] = rating_record.rating

        return entries

    @classmethod
    def create(cls, author, subject, content):
        """For creating a new post."""
        entry = cls(author=author,
                    subject=subject,
                    content=content,
                    likes=0,
                    dislikes=0)
        entry.put()
        return entry

    @classmethod
    def update_by_id(cls, post_id, subject, content):
        """For updating the subject and content of a blog entry."""
        entry = cls.get_by_id(post_id)
        entry.subject = subject
        entry.content = content
        entry.put()

    @classmethod
    def delete_by_id(cls, post_id):
        """For deleting a specific blog entry."""
        entry = cls.get_by_id(post_id)
        entry.key.delete()

    @classmethod
    def increment_like(cls, post_id):
        """For incrementing the number of likes a given blog entry has."""
        record = cls.by_id(post_id)
        record.likes += 1
        record.put()
        return record.likes

    @classmethod
    def increment_dislike(cls, post_id):
        """For incrementing the number of dislikes a given blog entry has."""
        record = cls.by_id(post_id)
        record.dislikes += 1
        record.put()
        return record.dislikes


class Comment(ndb.Model):
    """Datastore for blog comments."""

    post_id = ndb.StringProperty(required = True)
    author = ndb.StringProperty(required = True)
    commenter = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, id):
        return cls.get_by_id(id)

    @classmethod
    def by_post_id(cls, post_id):
        comment = cls.query(cls.post_id == post_id).get()
        return comment

    @classmethod
    def by_postid_dict(cls, post_id):
        """For converting a set of comments to a list of dictionaries."""
        query = cls.query(cls.post_id == post_id)
        all_comments = query.order(cls.created)
        all_comments_dict = [{"comment_id": str(record.key.id()),
                              "post_id": record.post_id,
                              "author": record.author,
                              "commenter": record.commenter,
                              "content": record.content,
                              "created": record.created.strftime("%b %d, %Y")
                             } for record in all_comments]
        return all_comments_dict

    @classmethod
    def create(cls, post_id, author, commenter, content):
        """For creating a new comment."""
        comment = cls(post_id=post_id,
                      author=author,
                      commenter=commenter,
                      content=content)
        comment.put()
        return comment

    @classmethod
    def update(cls, comment_id, new_content):
        """For updating the content of a specific comment."""
        comment = cls.by_id(comment_id)
        comment.content = new_content
        comment.put()

    @classmethod
    def delete_all_by_postid(cls, post_id):
        """For deleting all the comments associated with a blog entry."""
        comments = cls.query(cls.post_id == post_id)
        for comment in comments:
            comment.key.delete()

    @classmethod
    def delete_by_id(cls, comment_id):
        """For deleting a specific comment."""
        comment = cls.get_by_id(comment_id)
        comment.key.delete()
