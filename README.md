# Task Management App

A full-stack task management application with FastAPI backend and vanilla JavaScript frontend.

## Project Structure

```
DayTasks/
├── backend/          # FastAPI backend with MongoDB
│   ├── main.py       # FastAPI application
│   ├── database.py  # MongoDB connection
│   ├── models.py    # Database models
│   ├── schemas.py   # Pydantic schemas
│   └── routes/      # API routes
└── frontend/         # HTML/CSS/JS frontend
    ├── index.html
    ├── style.css
    └── script.js
```

## Setup Instructions

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start MongoDB:**
   - Make sure MongoDB is running on `localhost:27017`
   - Or update `MONGODB_URL` in `backend/database.py`

3. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`
   - API docs: `http://127.0.0.1:8000/docs`

### Frontend Setup

**Why a local server is needed:**
- Browsers block HTTP requests from `file://` protocol for security
- Opening `index.html` directly won't be able to connect to the backend
- A local server makes the frontend accessible via `http://` which can connect to the backend

**Option 1: Use Python HTTP Server (Easiest - Just double-click!)**
```bash
cd frontend
python -m http.server 8080
```
Or simply double-click `start-server.bat` (Windows) or run `start-server.sh` (Mac/Linux)

Then open: `http://localhost:8080` in your browser

**Option 2: Use VS Code Live Server**
- Install "Live Server" extension in VS Code
- Right-click on `index.html` → "Open with Live Server"

**Option 2: Use VS Code Live Server**
- Install "Live Server" extension in VS Code
- Right-click on `index.html` → "Open with Live Server"

**Option 3: Use Node.js http-server**
```bash
npx http-server frontend -p 8080
```

## API Endpoints

- `POST /tasks` - Create a new task
- `GET /tasks` - Get all tasks
- `PUT /tasks/{id}` - Toggle task completion
- `DELETE /tasks/{id}` - Delete a task

## Troubleshooting

1. **CORS errors:** Make sure you're using a local server (not file://)
2. **Backend not responding:** Check if MongoDB is running and FastAPI server is started
3. **Connection refused:** Verify the backend is running on `http://127.0.0.1:8000`

