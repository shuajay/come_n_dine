#for non authentication operations
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Books, Borrower
from app import db

# initiate the blueprint
main = Blueprint('main', __name__)

#route for landing page
@main.route('/')
def index():
    return render_template('login.html')

#route for home after successful login
@main.route('/home')
def home():
    return render_template('index.html')

#route for borrowing books
@main.route('/borrowBooks')
def borrowBooks():
    return render_template('borrow.html')

@main.route('/borrowBooks', methods=['POST'])
def borrow_post():
    #validate the borrower details using the borrow form details
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    book_id = request.form.get('book_id')
    book_title = request.form.get('book_title')
    tape_number = request.form.get('tape_number')
    date_of_issue = request.form.get('date_of_issue')
    
    #check for the borrower details
    borrower_details = Borrower.query.filter_by(book_id=book_id).first()
    
    #if it returns a book making use of the uniques code then book already in borrowed
    if borrower_details:
        flash('Book already borrowed')
        return redirect(url_for('main.borrowBooks'))

    #create new borrower record
    new_borrower = Borrower(name=name, phone_number=phone_number, address=address, book_id=book_id, book_title=book_title, tape_number=tape_number, date_of_issue=date_of_issue)

    #add the new book to the database
    db.session.add(new_borrower)
    db.session.commit()
    
    #message displayed if you have successfully added a new borrower
    flash('Borrower details captured')
    return redirect(url_for('main.borrowBooks'))


#route for available books
@main.route('/availableBooks')
def availableBooks():
    #query all the available books in the database
    bookList = Books.query.all()
    return render_template('available.html', bookList=bookList)

#route to see all the books that are in the system whether borrowed or not
@main.route('/storehouse')
def storehouse():
    allbooks = Books.query.all()
    return render_template('storehouse.html', allbooks=allbooks)

#route for currently borrowed books
@main.route('/borrowedBooks')
def borrowedBooks():
    #query details of borrowers and books borrowed
    borrowerList = Borrower.query.all()
    return render_template('borrowed.html', borrowerList=borrowerList)

#route for deleting
@main.route('/deleteBorrower')
def deleteBorrower():
    id = Borrower.id
    user_to_delete = Borrower.query.filter_by(id=id).first()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Borrower deleted successfully!!")
        borrowerList = Borrower.query.all()
        return render_template('borrowed.html', borrowerList=borrowerList, id=id)
        
    except:
        flash("Problem deleting Borrower details, Please try again!!")
        return render_template('borrowed.html', borrowerList=borrowerList, id=id)

#route for adding a new book
@main.route('/addBook')
def addBook():
    return render_template('addBook.html')


#route to handle the add book POST form data
@main.route('/addBook', methods=['POST'])
def addBook_post():
    #validate the book details being input into the form fields
    book_id = request.form.get('book_id')
    book_title = request.form.get('book_title')
    tape_number = request.form.get('tape_number')
    shelf_number = request.form.get('shelf_number')

    #  make use of the book_id to check if there is an existing book in the database
    book_details = Books.query.filter_by(book_id=book_id).first()
    
    #if it returns a book making use of the uniques code then book already in database
    if book_details:
        flash('Book already in database')
        return redirect(url_for('main.addBook'))

    #create new book
    new_book = Books(book_id=book_id, book_title=book_title, tape_number=tape_number, shelf_number=shelf_number)

    #add the new book to the database
    db.session.add(new_book)
    db.session.commit()
    
    # display the message if the book has been successfully added
    flash('Book successfully added')
    return redirect(url_for('main.addBook'))