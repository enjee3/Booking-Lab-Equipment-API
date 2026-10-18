# Lab Equipment Booking API

A backend project built with FastAPI for managing lab equipment.
Booking features are planned.

## Current features

- Check API health.
- List equipment.
- Find equipment by ID.
- Create equipment with validated names and locations.

## API endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | /health | Check API health |
| GET | /equipment | List equipment |
| GET | /equipment/{equipment_id} | Find equipment |
| POST | /equipment | Create equipment |

## Run locally

In Windows Command Prompt, run these commands from the project folder:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API.

## Current limitations

Equipment is stored in memory and resets when the server restarts.
Database storage, authentication, and booking features are not implemented yet.