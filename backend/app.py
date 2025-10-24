from flask import Flask, requestfrom flask import Flask

from flask_sqlalchemy import SQLAlchemyfrom flask_sqlalchemy import SQLAlchemy

from flask_cors import CORSfrom flask_cors import CORS

import osimport os



app = Flask(__name__)app = Flask(__name__)

CORS(app)CORS(app)



# Configure PostgreSQL connection# Configure PostgreSQL connection

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/readingtracker')app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/readingtracker')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Falseapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)db = SQLAlchemy(app)



class Book(db.Model):class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120), nullable=False)    title = db.Column(db.String(120), nullable=False)

    author = db.Column(db.String(120), nullable=False)    author = db.Column(db.String(120), nullable=False)

    total_pages = db.Column(db.Integer, nullable=False)    total_pages = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), nullable=False, default='To be read')  # 'To be read', 'Reading', 'Read Done'    status = db.Column(db.String(20), nullable=False, default='To be read')  # 'To be read', 'Reading', 'Read Done'



class ReadingLog(db.Model):class ReadingLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)    date = db.Column(db.Date, nullable=False)

    pages_read = db.Column(db.Integer, nullable=False)    pages_read = db.Column(db.Integer, nullable=False)

    book = db.relationship('Book', backref=db.backref('logs', lazy=True))    book = db.relationship('Book', backref=db.backref('logs', lazy=True))



@app.route('/api/books', methods=['GET'])@app.route('/api/books', methods=['GET'])

def get_books():def get_books():

    books = Book.query.all()    books = Book.query.all()

    books_with_progress = []    books_with_progress = []

        

    for book in books:    for book in books:

        # Calculate total pages read from logs        # Calculate total pages read from logs

        total_pages_read = db.session.query(db.func.sum(ReadingLog.pages_read))\        total_pages_read = db.session.query(db.func.sum(ReadingLog.pages_read))\

                          .filter(ReadingLog.book_id == book.id).scalar() or 0                          .filter(ReadingLog.book_id == book.id).scalar() or 0

                

        # Calculate pending pages        # Calculate pending pages

        pending_pages = max(0, book.total_pages - total_pages_read)        pending_pages = max(0, book.total_pages - total_pages_read)

                

        # Calculate progress percentage        # Calculate progress percentage

        progress_percentage = (total_pages_read / book.total_pages * 100) if book.total_pages > 0 else 0        progress_percentage = (total_pages_read / book.total_pages * 100) if book.total_pages > 0 else 0

                

        books_with_progress.append({        books_with_progress.append({

            'id': book.id,            'id': book.id,

            'title': book.title,            'title': book.title,

            'author': book.author,            'author': book.author,

            'total_pages': book.total_pages,            'total_pages': book.total_pages,

            'status': book.status,            'status': book.status,

            'pages_read': total_pages_read,            'pages_read': total_pages_read,

            'pending_pages': pending_pages,            'pending_pages': pending_pages,

            'progress_percentage': round(progress_percentage, 1)            'progress_percentage': round(progress_percentage, 1)

        })        })

        

    return {'books': books_with_progress}    return {'books': books_with_progress}



@app.route('/api/books', methods=['POST'])@app.route('/api/books', methods=['POST'])

def add_book():def add_book():

    data = request.json    from flask import request

    status = data.get('status', 'To be read')  # Default status    data = request.json

    book = Book(title=data['title'], author=data['author'], total_pages=data['total_pages'], status=status)    status = data.get('status', 'To be read')  # Default status

    db.session.add(book)    book = Book(title=data['title'], author=data['author'], total_pages=data['total_pages'], status=status)

    db.session.commit()    db.session.add(book)

    return {'id': book.id}, 201    db.session.commit()

    return {'id': book.id}, 201

@app.route('/api/books/<int:book_id>/status', methods=['PUT'])

def update_book_status(book_id):@app.route('/api/books/<int:book_id>/status', methods=['PUT'])

    data = request.jsondef update_book_status(book_id):

    book = Book.query.get_or_404(book_id)    from flask import request

    if 'status' in data:    data = request.json

        book.status = data['status']    book = Book.query.get_or_404(book_id)

        db.session.commit()    if 'status' in data:

        return {'message': 'Status updated successfully'}        book.status = data['status']

    return {'error': 'Status not provided'}, 400        db.session.commit()

        return {'message': 'Status updated successfully'}

@app.route('/api/stats', methods=['GET'])    return {'error': 'Status not provided'}, 400

def get_reading_stats():

    books = Book.query.all()@app.route('/api/stats', methods=['GET'])

    total_books = len(books)def get_reading_stats():

        books = Book.query.all()

    # Count by status    total_books = len(books)

    to_read_count = len([b for b in books if b.status == 'To be read'])    

    reading_count = len([b for b in books if b.status == 'Reading'])    # Count by status

    completed_count = len([b for b in books if b.status == 'Read Done'])    to_read_count = len([b for b in books if b.status == 'To be read'])

        reading_count = len([b for b in books if b.status == 'Reading'])

    # Calculate total pages and reading progress    completed_count = len([b for b in books if b.status == 'Read Done'])

    total_pages = sum(book.total_pages for book in books)    

    total_pages_read = 0    # Calculate total pages and reading progress

    total_pending_pages = 0    total_pages = sum(book.total_pages for book in books)

        total_pages_read = 0

    for book in books:    total_pending_pages = 0

        pages_read = db.session.query(db.func.sum(ReadingLog.pages_read))\    

                    .filter(ReadingLog.book_id == book.id).scalar() or 0    for book in books:

        total_pages_read += pages_read        pages_read = db.session.query(db.func.sum(ReadingLog.pages_read))\

        total_pending_pages += max(0, book.total_pages - pages_read)                    .filter(ReadingLog.book_id == book.id).scalar() or 0

            total_pages_read += pages_read

    overall_progress = (total_pages_read / total_pages * 100) if total_pages > 0 else 0        total_pending_pages += max(0, book.total_pages - pages_read)

        

    return {    overall_progress = (total_pages_read / total_pages * 100) if total_pages > 0 else 0

        'total_books': total_books,    

        'to_read_count': to_read_count,    return {

        'reading_count': reading_count,        'total_books': total_books,

        'completed_count': completed_count,        'to_read_count': to_read_count,

        'total_pages': total_pages,        'reading_count': reading_count,

        'total_pages_read': total_pages_read,        'completed_count': completed_count,

        'total_pending_pages': total_pending_pages,        'total_pages': total_pages,

        'overall_progress': round(overall_progress, 1)        'total_pages_read': total_pages_read,

    }        'total_pending_pages': total_pending_pages,

        'overall_progress': round(overall_progress, 1)

@app.route('/api/logs', methods=['POST'])    }

def add_log():

    data = request.json@app.route('/api/logs', methods=['POST'])

    log = ReadingLog(book_id=data['book_id'], date=data['date'], pages_read=data['pages_read'])def add_log():

    db.session.add(log)    from flask import request

    db.session.commit()    data = request.json

    return {'id': log.id}, 201    log = ReadingLog(book_id=data['book_id'], date=data['date'], pages_read=data['pages_read'])

    db.session.add(log)

@app.route('/api/logs/<int:book_id>', methods=['GET'])    db.session.commit()

def get_logs(book_id):    return {'id': log.id}, 201

    logs = ReadingLog.query.filter_by(book_id=book_id).all()

    return {'logs': [ {'id': l.id, 'date': l.date.isoformat(), 'pages_read': l.pages_read} for l in logs ]}@app.route('/api/logs/<int:book_id>', methods=['GET'])

def get_logs(book_id):

if __name__ == '__main__':    logs = ReadingLog.query.filter_by(book_id=book_id).all()

    app.run(debug=True)    return {'logs': [ {'id': l.id, 'date': l.date.isoformat(), 'pages_read': l.pages_read} for l in logs ]}

if __name__ == '__main__':
    app.run(debug=True)
