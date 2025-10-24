from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configure PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/readingtracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='To be read')

class ReadingLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    pages_read = db.Column(db.Integer, nullable=False)
    book = db.relationship('Book', backref=db.backref('logs', lazy=True))

@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_with_progress = []
    
    for book in books:
        total_pages_read = db.session.query(db.func.sum(ReadingLog.pages_read)).filter(ReadingLog.book_id == book.id).scalar() or 0
        pending_pages = max(0, book.total_pages - total_pages_read)
        progress_percentage = (total_pages_read / book.total_pages * 100) if book.total_pages > 0 else 0
        
        books_with_progress.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'total_pages': book.total_pages,
            'status': book.status,
            'pages_read': total_pages_read,
            'pending_pages': pending_pages,
            'progress_percentage': round(progress_percentage, 1)
        })
    
    return {'books': books_with_progress}

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    status = data.get('status', 'To be read')
    book = Book(title=data['title'], author=data['author'], total_pages=data['total_pages'], status=status)
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}, 201

@app.route('/api/books/<int:book_id>/status', methods=['PUT'])
def update_book_status(book_id):
    data = request.json
    book = Book.query.get_or_404(book_id)
    if 'status' in data:
        book.status = data['status']
        db.session.commit()
        return {'message': 'Status updated successfully'}
    return {'error': 'Status not provided'}, 400

@app.route('/api/stats', methods=['GET'])
def get_reading_stats():
    books = Book.query.all()
    total_books = len(books)
    
    to_read_count = len([b for b in books if b.status == 'To be read'])
    reading_count = len([b for b in books if b.status == 'Reading'])
    completed_count = len([b for b in books if b.status == 'Read Done'])
    
    total_pages = sum(book.total_pages for book in books)
    total_pages_read = 0
    total_pending_pages = 0
    
    for book in books:
        pages_read = db.session.query(db.func.sum(ReadingLog.pages_read)).filter(ReadingLog.book_id == book.id).scalar() or 0
        total_pages_read += pages_read
        total_pending_pages += max(0, book.total_pages - pages_read)
    
    overall_progress = (total_pages_read / total_pages * 100) if total_pages > 0 else 0
    
    return {
        'total_books': total_books,
        'to_read_count': to_read_count,
        'reading_count': reading_count,
        'completed_count': completed_count,
        'total_pages': total_pages,
        'total_pages_read': total_pages_read,
        'total_pending_pages': total_pending_pages,
        'overall_progress': round(overall_progress, 1)
    }

@app.route('/api/logs', methods=['POST'])
def add_log():
    data = request.json
    log = ReadingLog(book_id=data['book_id'], date=data['date'], pages_read=data['pages_read'])
    db.session.add(log)
    db.session.commit()
    return {'id': log.id}, 201

@app.route('/api/logs/<int:book_id>', methods=['GET'])
def get_logs(book_id):
    logs = ReadingLog.query.filter_by(book_id=book_id).all()
    return {'logs': [ {'id': l.id, 'date': l.date.isoformat(), 'pages_read': l.pages_read} for l in logs ]}

if __name__ == '__main__':
    app.run(debug=True)
