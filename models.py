from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    #id column
    id = db.Column(db.Integer, primary_key = True)
    #username column
    name = db.Column(db.String(50), nullable=False)
    #email column
    email = db.Column(db.String(100), unique = True, nullable=False)
    #password column
    password = db.Column(db.String(12), nullable=False)


class Books(UserMixin, db.Model):
    #book id uniquely identified that should of the form MoTHB3-int
    book_id = db.Column(db.String(20), primary_key=True, unique=True)
    #title column
    book_title = db.Column(db.String(200))
    #tape number column
    tape_number = db.Column(db.String(8))
    #shelf_number column
    shelf_number = db.Column(db.String(12))

    #create a one to many relationship
    borrowers = db.relationship('Borrower', backref='books')
    

class Borrower(UserMixin, db.Model):
    #id column
    id = db.Column(db.Integer, primary_key=True)
    #name column
    name = db.Column(db.String(75), nullable=False)
    #phone column
    phone_number = db.Column(db.String(10), nullable=False)
    #address column
    address = db.Column(db.String(500), nullable=False)
    #book title
    book_title = db.Column(db.String(200), nullable=False)
    #tape_number
    tape_number = db.Column(db.String(8), nullable=False)
    #date of issue column
    date_of_issue = db.Column(db.Text, nullable=False)
    #foreign key from the books table
    book_id = db.Column(db.String, db.ForeignKey('books.book_id'))