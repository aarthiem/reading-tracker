# 📚 My Reading Tracker

A modern web application for tracking your reading progress built with React frontend and Flask backend. Keep track of your books, reading sessions, and monitor your reading goals with detailed statistics and progress visualization.

![Reading Tracker](https://img.shields.io/badge/Status-Active-green)
![React](https://img.shields.io/badge/Frontend-React-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-red)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)

## ✨ Features

### 📖 Book Management
- **Add Books** - Add books with title, author, total pages, and initial reading status
- **Reading Status Tracking** - Three status levels: "To be read", "Reading", "Read Done"
- **Visual Status Indicators** - Color-coded badges for quick status identification
- **Progress Visualization** - Beautiful progress bars showing completion percentage

### 📊 Reading Progress Tracking
- **Reading Logs** - Track daily reading sessions with date and pages read
- **Pending Pages** - Automatically calculates remaining pages for each book
- **Progress Percentage** - Shows completion percentage for individual books
- **Reading History** - View all your reading sessions for each book

### 📈 Statistics Dashboard
- **Overall Statistics** - Total books in each status category
- **Reading Progress** - Total pages read vs pages pending across your library
- **Completion Tracking** - Overall progress percentage across all books
- **Real-time Updates** - Statistics update automatically as you log progress

### 🎨 Modern UI/UX
- **Beautiful Design** - Modern gradient background with clean white cards
- **Responsive Layout** - Works perfectly on desktop, tablet, and mobile
- **Interactive Elements** - Smooth animations and hover effects
- **Intuitive Interface** - Easy-to-use forms and navigation

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **PostgreSQL** database (local or Azure)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd myreadingtracker
```

### 2. Backend Setup
```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set database URL (replace with your credentials)
$env:DATABASE_URL = 'postgresql://username:password@host:5432/database?sslmode=require'

# Initialize database tables
python init_db.py

# Start the Flask server
python app.py
```

### 3. Frontend Setup
```bash
# Navigate to frontend folder (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

### 4. Open Your Browser
Navigate to `http://localhost:3000` to start using your Reading Tracker!

## 🗂️ Project Structure

```
myreadingtracker/
├── backend/                    # Flask API server
│   ├── app.py                 # Main Flask application
│   ├── init_db.py             # Database initialization script
│   ├── migrate_status.py      # Migration script for status feature
│   ├── requirements.txt       # Python dependencies
│   ├── schema/               # Database schema files
│   │   ├── init_tables.sql   # Initial table creation
│   │   └── add_status_column.sql # Status column migration
│   └── venv/                 # Virtual environment
├── frontend/                  # React application
│   ├── public/               # Static files
│   ├── src/                  # React source code
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   └── index.js         # React entry point
│   ├── package.json         # Node dependencies
│   └── node_modules/        # Node packages
├── docker-compose.yml        # Docker setup for PostgreSQL
├── READING_PROGRESS_FEATURE.md # Feature documentation
└── README.md                # This file
```

## 🎯 API Endpoints

### Books
- `GET /api/books` - Get all books with progress information
- `POST /api/books` - Add a new book
- `PUT /api/books/{id}/status` - Update book reading status

### Reading Logs
- `GET /api/logs/{book_id}` - Get reading logs for a specific book
- `POST /api/logs` - Add a new reading log entry

### Statistics
- `GET /api/stats` - Get overall reading statistics

## 🎨 Screenshots

### Dashboard View
Beautiful statistics dashboard showing your reading progress across all books.

### Book Management
Clean interface for managing your book collection with status tracking.

### Progress Tracking
Detailed progress visualization with animated progress bars.

## 🔧 Configuration

### Database Setup

#### Option 1: Local PostgreSQL
```bash
# Install PostgreSQL locally
# Create database and user
psql -U postgres -c "CREATE USER reader WITH PASSWORD 'password';"
psql -U postgres -c "CREATE DATABASE readingtracker OWNER reader;"

# Set environment variable
$env:DATABASE_URL = 'postgresql://reader:password@localhost:5432/readingtracker'
```

#### Option 2: Azure PostgreSQL
```bash
# Create Azure PostgreSQL Flexible Server
az postgres flexible-server create \
  --resource-group myResourceGroup \
  --name readingtracker-server \
  --location eastus \
  --admin-user reader \
  --admin-password YourSecurePassword

# Set environment variable
$env:DATABASE_URL = 'postgresql://reader:password@readingtracker-server.postgres.database.azure.com:5432/readingtracker?sslmode=require'
```

#### Option 3: Docker PostgreSQL
```bash
# Use the included docker-compose.yml
docker-compose up -d

# Set environment variable for local Docker
$env:DATABASE_URL = 'postgresql://reader:readerpass@localhost:5432/readingtracker'
```

## 🛠️ Development

### Adding New Features
1. **Backend**: Add new endpoints in `app.py`
2. **Frontend**: Update React components in `src/App.js`
3. **Database**: Add migration scripts in `schema/` folder
4. **Styling**: Update CSS in `src/App.css`

### Running Tests
```bash
# Backend tests (if implemented)
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## 🔄 Recent Updates

### Version 2.0 - Progress Tracking
- ✅ Added reading status tracking (To be read, Reading, Read Done)
- ✅ Implemented pending pages calculation
- ✅ Added progress percentage tracking
- ✅ Enhanced statistics dashboard
- ✅ Beautiful progress bars and visual indicators

### Version 1.0 - Initial Release
- ✅ Basic book management
- ✅ Reading log tracking
- ✅ React frontend with Flask backend
- ✅ PostgreSQL database integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check your DATABASE_URL format
echo $env:DATABASE_URL

# Verify PostgreSQL is running
# For local: Check PostgreSQL service
# For Azure: Check firewall rules and connection string
```

**Frontend Not Loading**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Backend API Errors**
```bash
# Check Flask is running on port 5000
curl http://localhost:5000/api/books

# Verify virtual environment is activated
which python  # Should show venv path
```

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the feature documentation in `READING_PROGRESS_FEATURE.md`
3. Create an issue in the repository

---

**Happy Reading! 📚✨**

Built with ❤️ using React, Flask, and PostgreSQL