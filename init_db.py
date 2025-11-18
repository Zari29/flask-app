from app import db

# Create all tables defined in app.py
db.create_all()
print("SQLite database created successfully!")
