# BNHS-SHS Grade Management System

A modern, full-stack web application designed for **Bonga National High School - Senior High School (BNHS-SHS)**. This system digitizes and streamlines the management of student registries, curriculum setup, grade encoding, and the generation of official Learner's Progress Report Cards (SF9).

## 🌟 Features

- **Principal's Office Dashboard**: Manage the school's curriculum (Tracks, Strands, Subjects, Sections), oversee faculty rosters, manage academic terms, and review/approve submitted grade batches.
- **Teacher Portal**: Set up teaching loads, manage student enrollment, encode quarterly grades, and submit official grade batches for principal approval.
- **Adviser Capabilities**: Class advisers can view consolidated semester grades and instantly generate print-ready SF9 report cards for their advisory sections.
- **Historical Archiving**: Securely archive student sections at the end of the school year and automatically advance the academic term.

## 💻 Tech Stack

- **Frontend**: Vue 3, Vite, Tailwind CSS
- **Backend**: Python, FastAPI, SQLAlchemy ORM
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Tokens) with bcrypt password hashing

---

## 🚀 How to Run the Application

To run this application locally, you will need to open two separate terminal windows: one for the backend server and one for the frontend development server.

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/) installed.
- [Node.js & npm](https://nodejs.org/en/download/) installed.

### Step 1: Set up the Backend (FastAPI)

1. Open your first terminal and navigate to the backend directory:
   ```bash
   cd "c:\Users\Asus\Desktop\bnhs system\backend"
   ```

2. Create and activate a virtual environment (Windows):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required Python dependencies (Assuming you have a requirements.txt, otherwise install fastapi, uvicorn, sqlalchemy, etc.):
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database and populate it with default curriculum and dummy accounts:
   ```bash
   python seed.py
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   *The API will now be running at `http://localhost:8000`*

### Step 2: Set up the Frontend (Vue.js)

1. Open a second terminal and navigate to the frontend directory:
   ```bash
   cd "c:\Users\Asus\Desktop\bnhs system\frontend"
   ```

2. Install the Node modules:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The web app will now be running at `http://localhost:5173`*

### Step 3: Log in

Open your web browser and go to `http://localhost:5173`. You can log in using the default seeded accounts:
- **Principal Account**: ID: `PRIN-001` | Password: `password123`
- **Teacher Account**: ID: `TCH-001` | Password: `password123`