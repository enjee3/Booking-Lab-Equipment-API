import os
from pathlib import Path
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

# Read the .env file beside this Python file.
env_path = Path(__file__).resolve().with_name(".env")
load_dotenv(env_path, interpolate=False)

# Build the database connection details.
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
)

# Prepare a manager for database connections.
engine = create_engine(database_url, pool_pre_ping=True)
def get_db():
    with Session(engine) as session:
        yield session
# Run this check when we execute: python database.py
if __name__ == "__main__":
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_user, current_database()")
        ).one()

        print("Database connection successful")
        print(f"User: {result[0]}")
        print(f"Database: {result[1]}")