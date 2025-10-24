""""""

Init script to create database tables for the Flask backend.Init script to create database tables for the Flask backend.

Run this after starting the Postgres container (docker-compose up -d)Run this after starting the Postgres container (docker-compose up -d)



Usage:Usage:

  (in a virtualenv with requirements installed)  (in a virtualenv with requirements installed)

  python init_db.py  python init_db.py



The script reads DATABASE_URL from environment (e.g., postgresql://reader:readerpass@localhost:5432/readingtracker).The script reads DATABASE_URL from environment (e.g., postgresql://reader:readerpass@localhost:5432/readingtracker).

If not set, it will try the default used in the app.If not set, it will try the default used in the app.

""""""

import osimport os

import timeimport time



from app import db, appfrom app import db, app



DB_URL = os.getenv('DATABASE_URL')DB_URL = os.getenv('DATABASE_URL')

if DB_URL:if DB_URL:

    print(f"Using DATABASE_URL from environment: {DB_URL}")    print(f"Using DATABASE_URL from environment: {DB_URL}")

else:else:

    print("No DATABASE_URL in environment, using app default")    print("No DATABASE_URL in environment, using app default")



# Try to connect and create tables. Will retry a few times in case Postgres isn't ready yet.# Try to connect and create tables. Will retry a few times in case Postgres isn't ready yet.

max_attempts = 15max_attempts = 15

attempt = 0attempt = 0

while attempt < max_attempts:while attempt < max_attempts:

    try:    try:

        with app.app_context():        with app.app_context():

            db.create_all()            db.create_all()

        print("Database tables created successfully.")        print("Database tables created successfully.")

        break        break

    except Exception as e:    except Exception as e:

        attempt += 1        attempt += 1

        print(f"Attempt {attempt}/{max_attempts} failed: {e}")        print(f"Attempt {attempt}/{max_attempts} failed: {e}")

        time.sleep(2)        time.sleep(2)

else:else:

    print("Failed to create database tables after multiple attempts. Check Postgres is running and DATABASE_URL is correct.")    print("Failed to create database tables after multiple attempts. Check Postgres is running and DATABASE_URL is correct.")
