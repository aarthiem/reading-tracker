# 🚀 Deployment Guide

## Quick Deploy Commands

### Deploy to GitHub
```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/aarthiem/reading-tracker.git
git branch -M main
git push -u origin main
```

### Local Development Setup
```bash
# Clone the repository
git clone https://github.com/aarthiem/reading-tracker.git
cd reading-tracker

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
export DATABASE_URL="your-postgresql-connection-string"
python init_db.py
python app.py

# Frontend setup (in a new terminal)
cd frontend
npm install
npm start
```

### Environment Variables
1. Copy `backend/.env.example` to `backend/.env`
2. Update the `DATABASE_URL` with your PostgreSQL connection string

### Database Setup Options
- **Local PostgreSQL**: See README.md for setup instructions
- **Azure PostgreSQL**: Use the Azure CLI commands in README.md
- **Docker PostgreSQL**: Use the included docker-compose.yml

## Production Deployment

### Backend (Flask)
- Deploy to Heroku, Azure App Service, or AWS Elastic Beanstalk
- Set environment variables for DATABASE_URL
- Use production WSGI server like Gunicorn

### Frontend (React)
- Build: `npm run build`
- Deploy to Netlify, Vercel, or Azure Static Web Apps
- Update API_URL to point to production backend

### Database
- Use managed PostgreSQL service (Azure Database, AWS RDS, etc.)
- Run migration scripts if needed
- Set up automated backups