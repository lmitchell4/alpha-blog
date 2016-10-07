

# Alpha Blog

Alpha Blog is a blogging website that features basic blogging 
capabilities - including creating, editing, and deleting blog posts - 
and allows users to comment on and rate posts.

Click [here](https://alpha-blog-1.appspot.com/) to see a live example 
of the site.


## Running Alpha Blog

Alpha Blog was built with [Python 2.7.12](https://www.python.org/downloads/), 
the [webapp2](https://webapp2.readthedocs.io/en/latest/) 
Python web framework, and 
[Google App Engine](https://cloud.google.com/appengine/docs/python/). User 
account information and blog post information, including blog content, 
ratings, and comments, are stored using the 
[Google Datastore NDB Client Library](https://cloud.google.com/appengine/docs/python/ndb/). 

To run the website locally:

1. Fork or download the code from GitHub

2. Download and install [Google App Engine SDK](https://cloud.google.com/appengine/docs/python/download) 

3. Navigate to the directory containing Alpha Blog's yaml file and 
run the command dev_appserver.py ./
  ```
  > cd my_path/.../alpha-blog
  > dev_appserver.py ./
  ```

4. Open your browser and navigate to http://localhost:8080

Alpha Blog was designed to be run on the Google Cloud Platform. See 
[this link](https://cloud.google.com/appengine/docs/python/) for 
information on developing and deploying projects using the 
Google App Engine Python Standard Environment.



## Creating an account 

To create an account, click the "Signup" button on Alpha Blog's 
home page and enter the requested information. Usernames and passwords must 
be at least three characters long, and can contain letters, numbers, 
dashses (-), and underscores (_).


## Logging in to your account 

To log in to your account, click the "Login" button on the home page and 
enter your account information. Once you've successfully logged in, you will 
be redirected to your home page.

When you are logged in, your username will appear in the upper right 
corner of the screen. When you are looking at someone's blog, the 
author's name will appear on the left hand side of the blog's 
navigation bar.


## Creating, editing, and deleting blog posts

To create, edit, or delete blog posts, log in to your account and use the 
"New Post", "Edit", and "Delete" buttons. The "New Post" button is located 
on your home page, and the "Edit" and "Delete" buttons appear when you click 
on an individual post.

Note that you can only edit and delete your own posts!


## Commenting on a blog post

You can comment on any blog post - including your own - but you must be logged 
in first. You also must be logged in to edit and delete your own comments.

**Caution** - Currently, when the owner of a blog post deletes the post, all of the 
associated comments are also deleted, so be aware that your comments can 
disappear at any time!


## Rating a blog post

Click on the Like or Dislike buttons below an individual blog post to rate the post. 
As of right now, you can't change the rating that you give a post, so use your 
rating powers carefully! When you like a post, the word Like turns blue. When you 
dislike a post, the word Dislike turns red. You must be logged in to the site to rate 
a post, and you can't rate any of your own posts.



## License

This project is released under [the MIT License](https://github.com/lmitchell4/alpha-blog/blob/master/LICENSE).

