from flask import Flask
from flask import render_template
import bookdb

app = Flask(__name__)

db = bookdb.BookDB()


@app.route('/')
def books():
    # put code here that provides a list of books to a template named 
    # "book_list.html"
    books = db.titles()
    return render_template('book_list.html', books=books)
    pass


@app.route('/book/<book_id>/')
def book(book_id):
    # put code here that provides the details of a single book to a template 
    # named "book_detail.html"
    book = db.title_info(book_id)
    return render_template('book_detail.html', title=book['title'], author=book['author'], publisher=book['publisher'], isbn=book['isbn'])
    pass


if __name__ == '__main__':
    app.run(debug=True)
