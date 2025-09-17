# 🚀 Job-app

This prototype is a **dynamic job & internship aggregator** that fetches openings from multiple sources (LinkedIn, job boards, ATS systems) and displays them in a modern React frontend.

---

## ✨ Features

* 🔄 Automatic job sync every minute (configurable)
* 🗑 Duplicate detection & cleanup by job link
* 🔍 Filter & search by title, location, source
* 📄 Pagination with custom page size
* ⚡ FastAPI backend with MongoDB Atlas
* 🎨 React (Vite) frontend with clean UI

---

## 📂 Project Structure

```
careerforge/
│── backend/               # Python backend (FastAPI)
│   ├── main.py            # FastAPI app + routes
│   ├── api.py             # API keys (local only, do not commit!)
│   ├── websites/          # API fetchers (LinkedIn, internships, etc.)
│   └── database/          # db.py, insert.py, debug.py
│
│── frontend/              # React frontend (Vite)
│   ├── src/
│   │   ├── pages/Jobs.jsx # Main jobs UI
│   │   ├── components/    # Pagination, JobCard, etc.
│   │   └── lib/api.js     # Axios API client
│   └── index.css          # Styles
│
│── README.md
```

---

## ⚙️ Backend Setup

### 1. Create virtual environment

```bash
cd backend
python -m venv venv
```

Activate it:

* **Windows PowerShell**

  ```bash
  venv\Scripts\activate
  ```
* **macOS/Linux**

  ```bash
  source venv/bin/activate
  ```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB Atlas

* Create a free [MongoDB Atlas](https://www.mongodb.com/atlas) cluster
* Copy your connection string (URI)
* Put it inside `backend/database/db.py`, e.g.:

```python
uri = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

### 4. Run backend

```bash
uvicorn main:app --reload
```

✅ API available at: [http://localhost:8000](http://localhost:8000)
✅ Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🎨 Frontend Setup

### 1. Install dependencies

```bash
cd ../frontend
npm install
```

### 2. Configure API URL

Create `.env` in `frontend/`:

```
VITE_API_BASE=http://localhost:8000
```

### 3. Run frontend

```bash
npm run dev
```

✅ Opens at: [http://localhost:5173](http://localhost:5173)

---

## ✅ Quick Start

```bash
# backend
cd backend
venv\Scripts\activate   # or source venv/bin/activate
uvicorn main:app --reload

# frontend
cd ../frontend
npm run dev
```

Then open [http://localhost:5173](http://localhost:5173) 🎉

---
