import random

from flask import Flask, render_template
from Seminar_3.task_2.models import db, Book, Author, BookAuthor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("fill-db")
def fill_tables():
    count = 10
    for author in range(1, count + 1):
        new_author = Author(
            name=f'name{author}',
            surname = f'surname{author}'

        )
        db.session.add(new_author)

    for book in range(1, count + 1):
        new_book = Book(
            name=f'name{book}',
            year=random.randint(1900, 2023),
            quantity=random.randint(1, 100),
            author_id=random.randint(1, 5)
        )
        db.session.add(new_book)
    for i in range(1, count + 1):
        book_author = BookAuthor(
            book_id=random.randint(1, count),
            author_id=random.randint(1, count),
        )
        db.session.add(book_author)
    db.session.commit()


@app.route('/books/')
def all_books():
    books = Book.query.all()
    context = {'books': books}
    return render_template('books.html', **context)
