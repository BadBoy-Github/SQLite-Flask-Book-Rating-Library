from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

all_books = []

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    books = Book.query.all()
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_name = request.form.get("bookname")
        book_author = request.form.get("bookauthor")
        book_rating = request.form.get("bookrating")
        new_book = Book(title=book_name, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    if request.method == "POST":
        new_rating = request.form.get("new_rating")
        book = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        book.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))
    book = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    return render_template("edit.html", book=book)

@app.route("/delete/<int:book_id>")
def delete(book_id):
    book = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

