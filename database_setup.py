# database_setup.py

from models import init_db

if __name__ == "__main__":
    session = init_db()
    print("Database initialized.")
