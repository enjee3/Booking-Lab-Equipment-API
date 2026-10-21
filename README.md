# Lab Equipment Booking API

A backend project built with FastAPI, SQLAlchemy, and PostgreSQL.
Equipment management is implemented; booking features are planned.

## Current features

- Check API health.
- List equipment and find equipment by ID.
- Create equipment with validated names and locations.
- Update equipment details and active status.
- Store equipment in PostgreSQL so records survive API restarts.
- Track database schema changes with Alembic migrations.

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | /health | Check API health |
| GET | /equipment | List equipment |
| GET | /equipment/{equipment_id} | Find equipment |
| POST | /equipment | Create equipment |
| PUT | /equipment/{equipment_id} | Update equipment |

## Local setup on Windows

Prerequisites:
- Python 3.13 with the Windows Python launcher (`py`).
- PostgreSQL 18 installed and running.
- A local copy of this repository.

Run terminal commands in Windows Command Prompt.

### 1. Create the database account and database

For a fresh installation, connect as the PostgreSQL administrator:

```bat
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5432 -U postgres -d postgres
```

Inside psql, run these commands individually:

```text
CREATE ROLE lab_app WITH LOGIN;
\password lab_app
CREATE DATABASE lab_booking OWNER lab_app;
\q
```

The password command prompts you to choose the lab_app password.
Skip this section if the account and database already exist.

### 2. Install Python dependencies

From the project folder:

```bat
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configure the database connection

Create the local configuration file if it does not already exist:

```bat
if not exist .env copy .env.example .env
```

The example uses localhost, port 5432, database lab_booking,
and user lab_app. Adjust these settings in .env if necessary.

Save the lab_app password using a hidden prompt:

```bat
.venv\Scripts\python.exe -c "from getpass import getpass; from dotenv import set_key; set_key('.env', 'DB_PASSWORD', getpass('Enter lab_app password: '))"
```

Keep .env private. Commit only the placeholder .env.example.

### 4. Check the connection and apply migrations

Run these commands from the project folder:

```bat
.venv\Scripts\python.exe database.py
.venv\Scripts\python.exe init_db.py
```

`init_db.py` applies pending Alembic migrations to the database
configured in `.env`. On a fresh database, the initial migration
creates an empty equipment table.

Run `init_db.py` whenever you pull or create new migrations,
before starting the API.

To check migration status:

```bat
.venv\Scripts\python.exe -m alembic current
.venv\Scripts\python.exe -m alembic check
```

`current` displays the recorded migration version.
`check` reports whether Alembic detects schema differences
between the database and the SQLAlchemy models.

### 5. Start the API

```bat
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open [Swagger documentation](http://127.0.0.1:8000/docs).

## Resume development later

Ensure PostgreSQL is running. From the project folder, run:

```bat
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

## Manual persistence check

1. Create equipment using POST /equipment.
2. Note the id in the response body.
3. Update the record using PUT /equipment/{equipment_id}.
4. Stop and restart the API.
5. Retrieve the same ID and check that the updated values remain.

## Planned work

- Authentication and roles.
- Bookings and prevention of overlapping reservations.
- Database migrations.
- Automated tests, concurrency tests, and load testing.