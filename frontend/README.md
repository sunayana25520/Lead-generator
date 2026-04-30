# 🚀 Lead Generation Dashboard

A full-stack application that analyzes company websites and generates lead insights using automated scraping and signal detection.

---

## 🧩 Tech Stack

### 🔹 Frontend

* React.js
* HTML, CSS
* Axios

### 🔹 Backend

* FastAPI (Python)
* Playwright (Web Scraping)
* Async processing

### 🔹 Database

* SQLite

---

## ⚙️ Features

* 📂 Upload CSV file with company names & websites
* 🌐 Automatically scrape company websites
* 🔍 Detect signals:

  * Hiring activity
  * QA / Testing presence
  * SaaS / Product indicators
  * Website health
* 📊 Generate lead scores
* 📝 Provide descriptions for each company

---

## 📁 Project Structure

```id="s9kzqj"
project/
├── backend/
│   ├── main.py
│   ├── scraper.py
│   ├── utils.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```id="x2z9wd"
git clone https://github.com/RK805/LeadGenerationEngine.git
cd LeadGenerationEngine
```

---

### 2️⃣ Setup Backend

```id="l3n8av"
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on:
👉 http://127.0.0.1:8000

---

### 3️⃣ Setup Frontend

```id="y7pq1e"
cd frontend
npm install
npm start
```

Frontend runs on:
👉 http://localhost:3000

---

## 🔗 API Endpoints

### POST `/upload`

Upload CSV file to start analysis

### POST `/analyze`

Analyze companies and generate lead scores

---

## 📌 Example Input

```json id="r4bxzv"
[
  {
    "company": "ClickUp",
    "website": "https://clickup.com"
  }
]
```

---

## 📊 Output Includes

* Score
* Signals
* Description
* Health status

---


