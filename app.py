from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'library_management_secret_key'

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    available = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Book {self.title}>'

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    member_type = db.Column(db.String(20), nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Member {self.name}>'

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.String(20), unique=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    fine_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='Issued')
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships
    book = db.relationship('Book', backref=db.backref('issues', lazy=True))
    member = db.relationship('Member', backref=db.backref('issues', lazy=True))
    
    def __repr__(self):
        return f'<Issue {self.issue_id}>'

# Initialize the database
with app.app_context():
    db.create_all()
    
    # Add default books if the database is empty
    if Book.query.count() == 0:
        default_books = [
            Book(title="To Kill a Mockingbird", author="Harper Lee", isbn="978-0061120084", 
                 publisher="HarperCollins", publication_year=1960, category="fiction", quantity=5, available=5),
            Book(title="1984", author="George Orwell", isbn="978-0451524935", 
                 publisher="Signet Classic", publication_year=1949, category="fiction", quantity=5, available=5),
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="978-0743273565", 
                 publisher="Scribner", publication_year=1925, category="fiction", quantity=4, available=4),
            Book(title="Pride and Prejudice", author="Jane Austen", isbn="978-0141439518", 
                 publisher="Penguin Classics", publication_year=1813, category="literature", quantity=3, available=3),
            Book(title="The Catcher in the Rye", author="J.D. Salinger", isbn="978-0316769488", 
                 publisher="Little, Brown and Company", publication_year=1951, category="fiction", quantity=4, available=4),
            Book(title="The Hobbit", author="J.R.R. Tolkien", isbn="978-0547928227", 
                 publisher="Houghton Mifflin", publication_year=1937, category="fiction", quantity=5, available=5),
            Book(title="Sapiens: A Brief History of Humankind", author="Yuval Noah Harari", isbn="978-0062316097", 
                 publisher="Harper", publication_year=2014, category="non-fiction", quantity=3, available=3),
            Book(title="The Origin of Species", author="Charles Darwin", isbn="978-0451529060", 
                 publisher="Signet", publication_year=1859, category="science", quantity=2, available=2),
            Book(title="A Brief History of Time", author="Stephen Hawking", isbn="978-0553380163", 
                 publisher="Bantam", publication_year=1988, category="science", quantity=3, available=3),
            Book(title="The Art of War", author="Sun Tzu", isbn="978-1590302255", 
                 publisher="Shambhala", publication_year=500, category="non-fiction", quantity=4, available=4)
        ]
        
        try:
            for book in default_books:
                db.session.add(book)
            db.session.commit()
            print("Added 10 default books to the database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding default books: {str(e)}")
    
    # Add default members if the database is empty
    if Member.query.count() == 0:
        default_members = [
            Member(
                member_id="M001",
                name="Ansuman jena",
                email="ansumanjena2004@gmail.com",
                phone="9040784900",
                address="Rourkela",
                member_type="student",
                join_date=datetime.strptime("2023-01-15", "%Y-%m-%d").date()
            ),
            Member(
                member_id="M002",
                name="Sreyanshu Sekhar Mohanty",
                email="sreyanshusekhar2004@gmail.com",
                phone="7749954516",
                address="Bhadrak",
                member_type="faculty",
                join_date=datetime.strptime("2023-02-20", "%Y-%m-%d").date()
            ),
            Member(
                member_id="M003",
                name="Dipun Barik",
                email="dipunbarik2004@gmail.com",
                phone="9040234796",
                address="Keonjhar",
                member_type="student",
                join_date=datetime.strptime("2023-03-10", "%Y-%m-%d").date()
            ),
            Member(
                member_id="M004",
                name="Abhijit Rath",
                email="abhijitrath2004@gmail.com",
                phone="7205389498",
                address="Jajpur",
                member_type="student",
                join_date=datetime.strptime("2023-04-05", "%Y-%m-%d").date()
            )
        ]
        
        try:
            for member in default_members:
                db.session.add(member)
            db.session.commit()
            print("Added 5 default members to the database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding default members: {str(e)}")
    
    # Add default transactions if the database is empty
    if Issue.query.count() == 0 and Book.query.count() > 0 and Member.query.count() > 0:
        # Get some books and members to use in transactions
        books = Book.query.limit(5).all()
        members = Member.query.limit(3).all()
        
        # Create some default transaction records with different statuses
        default_issues = [
            # Returned books (completed transactions)
            Issue(
                issue_id="I001523",
                book_id=books[0].id,
                member_id=members[0].id,
                issue_date=datetime.strptime("2024-11-15", "%Y-%m-%d").date(),
                due_date=datetime.strptime("2025-01-28", "%Y-%m-%d").date(),
                return_date=datetime.strptime("2025-01-28", "%Y-%m-%d").date(),
                fine_amount=0.0,
                status="Returned",
                remarks="Returned on time"
            ),
            Issue(
                issue_id="I001624",
                book_id=books[1].id,
                member_id=members[1].id,
                issue_date=datetime.strptime("2025-02-10", "%Y-%m-%d").date(),
                due_date=datetime.strptime("2025-02-24", "%Y-%m-%d").date(),
                return_date=datetime.strptime("2025-03-01", "%Y-%m-%d").date(),
                fine_amount=3.5,
                status="Returned",
                remarks="Returned 5 days late, fine collected"
            ),
            # Currently issued books (active transactions)
            Issue(
                issue_id="I001725",
                book_id=books[2].id,
                member_id=members[2].id,
                issue_date=datetime.strptime("2025-03-05", "%Y-%m-%d").date(),
                due_date=datetime.strptime("2025-03-21", "%Y-%m-%d").date(),
                status="Issued"
            ),
            Issue(
                issue_id="I001826",
                book_id=books[3].id,
                member_id=members[0].id,
                issue_date=datetime.strptime("2025-01-10", "%Y-%m-%d").date(),
                due_date=datetime.strptime("2025-01-24", "%Y-%m-%d").date(),
                status="Issued"
            ),
            Issue(
                issue_id="I001927",
                book_id=books[4].id,
                member_id=members[1].id,
                issue_date=datetime.strptime("2025-02-12", "%Y-%m-%d").date(),
                due_date=datetime.strptime("2025-02-26", "%Y-%m-%d").date(),
                status="Issued"
            )
        ]
        
        try:
            # Update book availability for currently issued books
            for issue in default_issues:
                if issue.status == "Issued":
                    book = Book.query.get(issue.book_id)
                    if book.available > 0:
                        book.available -= 1
                db.session.add(issue)
            
            db.session.commit()
            print("Added 5 default transactions to the database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding default transactions: {str(e)}")

# Routes for Book CRUD operations
@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['bookTitle']
        author = request.form['author']
        isbn = request.form['isbn']
        publisher = request.form['publisher']
        publication_year = request.form['publicationYear']
        category = request.form['category']
        quantity = request.form['quantity']
        
        # Create new book
        new_book = Book(
            title=title,
            author=author,
            isbn=isbn,
            publisher=publisher,
            publication_year=publication_year,
            category=category,
            quantity=quantity,
            available=quantity
        )
        
        try:
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('books'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding book: {str(e)}', 'danger')
    
    return render_template('books.html')

@app.route('/books/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    books = Book.query.all()
    
    if request.method == 'POST':
        book.title = request.form['bookTitle']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.publisher = request.form['publisher']
        book.publication_year = request.form['publicationYear']
        book.category = request.form['category']
        book.quantity = request.form['quantity']
        
        try:
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('books'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating book: {str(e)}', 'danger')
    
    return render_template('books.html', book=book, books=books, edit_mode=True)

@app.route('/books/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {str(e)}', 'danger')
    
    return redirect(url_for('books'))

# Routes for Member CRUD operations
@app.route('/members')
def members():
    members = Member.query.all()
    return render_template('members.html', members=members)

@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        member_id = request.form['memberID']
        name = request.form['memberName']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        member_type = request.form['memberType']
        join_date = datetime.strptime(request.form['joinDate'], '%Y-%m-%d').date()
        
        # Create new member
        new_member = Member(
            member_id=member_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            member_type=member_type,
            join_date=join_date
        )
        
        try:
            db.session.add(new_member)
            db.session.commit()
            flash('Member added successfully!', 'success')
            return redirect(url_for('members'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding member: {str(e)}', 'danger')
    
    return render_template('members.html')

@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Member.query.get_or_404(id)
    members = Member.query.all()
    
    if request.method == 'POST':
        member.member_id = request.form['memberID']
        member.name = request.form['memberName']
        member.email = request.form['email']
        member.phone = request.form['phone']
        member.address = request.form['address']
        member.member_type = request.form['memberType']
        member.join_date = datetime.strptime(request.form['joinDate'], '%Y-%m-%d').date()
        
        try:
            db.session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('members'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating member: {str(e)}', 'danger')
    
    return render_template('members.html', member=member, members=members, edit_mode=True)

@app.route('/members/delete/<int:id>')
def delete_member(id):
    member = Member.query.get_or_404(id)
    
    try:
        db.session.delete(member)
        db.session.commit()
        flash('Member deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting member: {str(e)}', 'danger')
    
    return redirect(url_for('members'))

# Routes for Issue/Return CRUD operations
@app.route('/issues')
def issues():
    issues = Issue.query.all()
    return render_template('issue.html', issues=issues, current_date=date.today())

@app.route('/issues/add', methods=['GET', 'POST'])
def add_issue():
    if request.method == 'POST':
        issue_id = f"I{str(datetime.now().timestamp()).replace('.', '')[-6:]}"
        member_id = request.form['memberID']
        book_id = request.form['bookID']
        issue_date = datetime.strptime(request.form['issueDate'], '%Y-%m-%d').date()
        due_date = datetime.strptime(request.form['dueDate'], '%Y-%m-%d').date()
        
        # Get the book and member
        book = Book.query.filter_by(isbn=book_id).first() or Book.query.get(book_id)
        member = Member.query.filter_by(member_id=member_id).first() or Member.query.get(member_id)
        
        if not book:
            flash('Book not found!', 'danger')
            return redirect(url_for('issues'))
        
        if not member:
            flash('Member not found!', 'danger')
            return redirect(url_for('issues'))
        
        if book.available <= 0:
            flash('Book is not available for issue!', 'danger')
            return redirect(url_for('issues'))
        
        # Create new issue
        new_issue = Issue(
            issue_id=issue_id,
            book_id=book.id,
            member_id=member.id,
            issue_date=issue_date,
            due_date=due_date,
            status='Issued'
        )
        
        # Update book availability
        book.available -= 1
        
        try:
            db.session.add(new_issue)
            db.session.commit()
            flash('Book issued successfully!', 'success')
            return redirect(url_for('issues'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error issuing book: {str(e)}', 'danger')
    
    return render_template('issue.html')

@app.route('/issues/return', methods=['POST'])
def return_book():
    issue_id = request.form['issueID']
    return_date = datetime.strptime(request.form['returnDate'], '%Y-%m-%d').date()
    fine_amount = float(request.form['fineAmount'])
    remarks = request.form['remarks']
    
    issue = Issue.query.filter_by(issue_id=issue_id).first()
    
    if not issue:
        flash('Issue record not found!', 'danger')
        return redirect(url_for('issues'))
    
    if issue.status == 'Returned':
        flash('This book has already been returned!', 'warning')
        return redirect(url_for('issues'))
    
    # Update issue record
    issue.return_date = return_date
    issue.fine_amount = fine_amount
    issue.remarks = remarks
    issue.status = 'Returned'
    
    # Update book availability
    book = Book.query.get(issue.book_id)
    book.available += 1
    
    try:
        db.session.commit()
        flash('Book returned successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error returning book: {str(e)}', 'danger')
    
    return redirect(url_for('issues'))

# Home route
@app.route('/')
def index():
    book_count = Book.query.count()
    member_count = Member.query.count()
    issued_count = Issue.query.filter_by(status='Issued').count()
    available_count = sum([book.available for book in Book.query.all()])
    
    return render_template('index.html', 
                           book_count=book_count,
                           member_count=member_count,
                           issued_count=issued_count,
                           available_count=available_count)

# About route
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
