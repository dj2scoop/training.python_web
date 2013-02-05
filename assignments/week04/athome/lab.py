#!/usr/bin/python
#John Comstock
#Week 04

import os
import re
import bookdb
from cgi import escape
import base64

# HTML template for first page with list of books
body = """<html>
<head>
<title>Lab2</title>
</head>
<body>
<img src="data:image/png;base64,%s" height="150" width="150"><br>
<h1>Welcome to the book DB!</h1><br>
<h3><a href="books/%s">%s</a><br>
<a href="books/%s">%s</a><br>
<a href="books/%s">%s</a><br>
<a href="books/%s">%s</a><br>
<a href="books/%s">%s</a></h3><br>
</body>
</html>"""

# HTML template for supporting book pages
book_body = """<html>
<head>
<title>%s</title>
</head>
<body>
<img src="data:image/png;base64,%s" height="150" width="150"><br>
<h3>Title: %s<br>
Author: %s<br>
Publisher: %s<br>
ISBN: %s</h3><br>
</body>
</html>"""


def index(environ, start_response):
    """This function will be mounted on /lab.py and will display the book list page."""
        
    books = bookdb.BookDB()
    bTitles = books.titles()
    titles = get_titles(bTitles)
    ids = get_ids(bTitles)
    image = get_image('books.png')
    response_body = body % (
                image,
		ids[0], titles[0],
		ids[1], titles[1],
		ids[2], titles[2],
		ids[3], titles[3],
		ids[4], titles[4]
		)

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [response_body]

def get_ids(idList):
    """Gets the book ids to create links based on the books id."""
    idsList = []
    for ids in idList:
	idsList.append(ids['id'])
    return idsList

def get_titles(titles):
    """"Gets the book titles to display as the link name."""
    titleList = []
    for title in titles:
        titleList.append(title['title'])
    return titleList

# This code was co-opted from http://stackoverflow.com/questions/3715493/encoding-an-image-file-with-base64
def get_image(image):
    """Takes an image and returns a base64 encoded string."""
    src_dir = 'images'
    filename = os.path.join(src_dir, image)
    with open(filename, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

# Some of this code is from http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/
def books(environ, start_response):
    """Uses the 'myapp.url_args to get a book id and returns the information about the specific book related to the id."""

    args = environ['myapp.url_args']
    print args
    if args:
        book_id = escape(args[0])
    else:
        return not_found(environ, start_response)
   
    books = bookdb.BookDB()
    book_info = books.title_info(book_id)
    image = get_image('books3.png')
    response_body = book_body % (
                book_info['title'],
                image,
                book_info['title'], 
                book_info['author'],
                book_info['publisher'],
		book_info['isbn']
                )
 
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [response_body]

def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

# This code co-opted from http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/
# map urls to functions
urls = [
    (r'^$', index),
    (r'books/(id[1-5])$', books)
]

# This code is from http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/
def application(environ, start_response):
    """
    The main WSGI application. Dispatch the current request to
    the functions from the above and store the regular expression
    captures in the WSGI environment as `myapp.url_args` so that
    the functions fron above can access the url placeholders.

    If nothing matches call the `not_found` function.
    """
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['myapp.url_args'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
