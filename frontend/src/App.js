
import React, { useEffect, useState } from 'react';
import './App.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [books, setBooks] = useState([]);
  const [logs, setLogs] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [bookForm, setBookForm] = useState({ title: '', author: '', total_pages: '', status: 'To be read' });
  const [logForm, setLogForm] = useState({ date: '', pages_read: '' });
  const [overallStats, setOverallStats] = useState(null);

  useEffect(() => {
    fetchBooks();
    fetchOverallStats();
  }, []);

  const fetchBooks = async () => {
    const res = await fetch(`${API_URL}/books`);
    const data = await res.json();
    setBooks(data.books);
  };

  const fetchOverallStats = async () => {
    const res = await fetch(`${API_URL}/stats`);
    const data = await res.json();
    setOverallStats(data);
  };

  const fetchLogs = async (bookId) => {
    const res = await fetch(`${API_URL}/logs/${bookId}`);
    const data = await res.json();
    setLogs(data.logs);
  };

  const handleBookFormChange = (e) => {
    setBookForm({ ...bookForm, [e.target.name]: e.target.value });
  };

  const handleLogFormChange = (e) => {
    setLogForm({ ...logForm, [e.target.name]: e.target.value });
  };

  const handleAddBook = async (e) => {
    e.preventDefault();
    await fetch(`${API_URL}/books`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: bookForm.title,
        author: bookForm.author,
        total_pages: parseInt(bookForm.total_pages),
        status: bookForm.status
      })
    });
    setBookForm({ title: '', author: '', total_pages: '', status: 'To be read' });
    fetchBooks();
    fetchOverallStats();
  };

  const handleAddLog = async (e) => {
    e.preventDefault();
    if (!selectedBook) return;
    await fetch(`${API_URL}/logs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        book_id: selectedBook.id,
        date: logForm.date,
        pages_read: parseInt(logForm.pages_read)
      })
    });
    setLogForm({ date: '', pages_read: '' });
    fetchLogs(selectedBook.id);
    fetchBooks(); // Refresh to update progress
    fetchOverallStats();
  };

  const handleSelectBook = (book) => {
    setSelectedBook(book);
    fetchLogs(book.id);
  };

  const handleStatusChange = async (bookId, newStatus) => {
    await fetch(`${API_URL}/books/${bookId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    fetchBooks();
    if (selectedBook && selectedBook.id === bookId) {
      setSelectedBook({ ...selectedBook, status: newStatus });
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'To be read': return 'to-be-read';
      case 'Reading': return 'reading';
      case 'Read Done': return 'read-done';
      default: return 'to-be-read';
    }
  };

  const getBookStats = () => {
    const toRead = books.filter(book => book.status === 'To be read').length;
    const reading = books.filter(book => book.status === 'Reading').length;
    const completed = books.filter(book => book.status === 'Read Done').length;
    const totalPages = books.reduce((sum, book) => sum + book.total_pages, 0);
    const completedPages = books.filter(book => book.status === 'Read Done').reduce((sum, book) => sum + book.total_pages, 0);
    
    return { toRead, reading, completed, totalPages, completedPages };
  };

  const stats = getBookStats();

  return (
    <div className="App">
      <h1>📚 Reading Tracker</h1>
      
      {books.length > 0 && overallStats && (
        <div className="section" style={{ marginBottom: '20px' }}>
          <h2>📊 Reading Statistics</h2>
          <div className="stats-container">
            <div className="stat-item">
              <div className="stat-number">{overallStats.to_read_count}</div>
              <div className="stat-label">To Read</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{overallStats.reading_count}</div>
              <div className="stat-label">Currently Reading</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{overallStats.completed_count}</div>
              <div className="stat-label">Completed</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{overallStats.total_pages_read}</div>
              <div className="stat-label">Pages Read</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{overallStats.total_pending_pages}</div>
              <div className="stat-label">Pages Pending</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{overallStats.overall_progress}%</div>
              <div className="stat-label">Overall Progress</div>
            </div>
          </div>
        </div>
      )}
      
      <div className="main-container">
        <div className="section">
          <h2>➕ Add New Book</h2>
          <form onSubmit={handleAddBook} className="form-container">
            <div className="form-group">
              <input 
                name="title" 
                placeholder="Book Title" 
                value={bookForm.title} 
                onChange={handleBookFormChange} 
                required 
              />
            </div>
            <div className="form-group">
              <input 
                name="author" 
                placeholder="Author Name" 
                value={bookForm.author} 
                onChange={handleBookFormChange} 
                required 
              />
            </div>
            <div className="form-group">
              <input 
                name="total_pages" 
                type="number" 
                placeholder="Total Pages" 
                value={bookForm.total_pages} 
                onChange={handleBookFormChange} 
                required 
              />
            </div>
            <div className="form-group">
              <select name="status" value={bookForm.status} onChange={handleBookFormChange}>
                <option value="To be read">📖 To be read</option>
                <option value="Reading">📘 Reading</option>
                <option value="Read Done">✅ Read Done</option>
              </select>
            </div>
            <button type="submit" className="btn">Add Book</button>
          </form>
          
          <h2>📚 My Books</h2>
          <ul className="book-list">
            {books.map(book => (
              <li key={book.id} className="book-item">
                <div className="book-info">
                  <button 
                    className={`book-button ${selectedBook?.id === book.id ? 'selected' : ''}`}
                    onClick={() => handleSelectBook(book)}
                  >
                    <strong>{book.title}</strong><br />
                    <small>by {book.author} • {book.total_pages} pages</small>
                    {book.pages_read > 0 && (
                      <div className="progress-info">
                        <small>
                          📖 {book.pages_read}/{book.total_pages} pages • 
                          📄 {book.pending_pages} pending • 
                          📊 {book.progress_percentage}% complete
                        </small>
                      </div>
                    )}
                  </button>
                  <span className={`status-badge ${getStatusColor(book.status)}`}>
                    {book.status}
                  </span>
                  <select 
                    value={book.status} 
                    onChange={(e) => handleStatusChange(book.id, e.target.value)}
                    className="status-select"
                  >
                    <option value="To be read">📖 To be read</option>
                    <option value="Reading">📘 Reading</option>
                    <option value="Read Done">✅ Read Done</option>
                  </select>
                </div>
                {book.pages_read > 0 && (
                  <div className="progress-bar-container">
                    <div 
                      className="progress-bar" 
                      style={{ width: `${Math.min(book.progress_percentage, 100)}%` }}
                    ></div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
        
        <div className="section">
          <h2>📊 Reading Progress</h2>
          {selectedBook ? (
            <>
              <div className="selected-book-title">
                📖 {selectedBook.title}
              </div>
              <form onSubmit={handleAddLog} className="form-container">
                <div className="form-group">
                  <input 
                    name="date" 
                    type="date" 
                    value={logForm.date} 
                    onChange={handleLogFormChange} 
                    required 
                  />
                </div>
                <div className="form-group">
                  <input 
                    name="pages_read" 
                    type="number" 
                    placeholder="Pages Read Today" 
                    value={logForm.pages_read} 
                    onChange={handleLogFormChange} 
                    required 
                  />
                </div>
                <button type="submit" className="btn">Log Progress</button>
              </form>
              
              <div className="logs-section">
                <h3>📈 Reading History</h3>
                <ul className="log-list">
                  {logs.map(log => (
                    <li key={log.id} className="log-item">
                      <span className="log-date">{log.date}</span>
                      <span className="log-pages">{log.pages_read} pages</span>
                    </li>
                  ))}
                </ul>
              </div>
            </>
          ) : (
            <div className="no-selection">
              👆 Select a book from the list to track your reading progress
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
