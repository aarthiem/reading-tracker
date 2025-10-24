"""
Migration script to add status column to existing books table.
Run this after updating your Flask app.py model.
"""
import os
from app import db, app

def migrate_add_status_column():
    with app.app_context():
        try:
            # Check if status column already exists
            result = db.engine.execute("SELECT column_name FROM information_schema.columns WHERE table_name='book' AND column_name='status'")
            if result.fetchone():
                print("Status column already exists.")
                return
            
            # Add the status column
            db.engine.execute("ALTER TABLE book ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'To be read'")
            print("Status column added successfully.")
            
        except Exception as e:
            print(f"Migration failed: {e}")
            print("You may need to drop and recreate tables, or run the migration manually.")

if __name__ == '__main__':
    migrate_add_status_column()