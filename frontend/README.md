# 🎨 CareerForge Frontend

This is the **React (Vite) frontend** for CareerForge.
It fetches job & internship data from the **FastAPI backend** and displays it with filters, pagination, and auto-refresh.

---

## ⚙️ Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Configure API URL

Create a `.env` file in the `frontend/` folder:

```
VITE_API_BASE=http://localhost:8000
```

This tells the frontend where to fetch jobs from (the backend).

### 3. Run development server

```bash
npm run dev
```

The app will open at: [http://localhost:5173](http://localhost:5173)

---

## 📂 Project Structure

```
frontend/
│── src/
│   ├── lib/
│   │   └── api.js        # Axios client to talk to backend API
│   │
│   ├── components/
│   │   ├── Pagination.jsx # Reusable pagination UI
│   │   └── JobCard.jsx    # Single job card UI (optional if used)
│   │
│   ├── pages/
│   │   └── Jobs.jsx       # Main page (fetches jobs + renders UI)
│   │
│   ├── App.jsx            # Router, entry point
│   ├── main.jsx           # React bootstrapper
│   └── index.css          # Global styles
│
└── .env                   # API base URL (not committed to git)
```

---

## 🔗 How the files connect

1. **`src/lib/api.js`**

   * Wraps `axios` to call the backend.
   * Example: `fetchJobs({ title, location, limit, offset })` → calls `http://localhost:8000/jobs`.

2. **`src/pages/Jobs.jsx`**

   * Main UI page.
   * Uses `fetchJobs` to load job data.
   * Handles filters (title, location, source), pagination, and auto-refresh.
   * Renders results using job cards.

3. **`src/components/Pagination.jsx`**

   * Displays page numbers + prev/next.
   * Used inside `Jobs.jsx` to navigate through job results.

4. **`src/components/JobCard.jsx`** (if present)

   * Simple card layout for one job posting.
   * Shows title, company, location, date, etc.

5. **`src/App.jsx`**

   * Sets up routing with `react-router-dom`.
   * Currently routes `/` → `Jobs` page.

6. **`src/main.jsx`**

   * Bootstraps React and renders `<App />` into `index.html`.

7. **`src/index.css`**

   * Global CSS (colors, cards, inputs, pagination styles).
   * Shared by all components.

---