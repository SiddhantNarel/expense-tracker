# 💰 Personal Expense Tracker

A full-stack **Personal Finance Tracker** with React frontend and Flask backend, using SQLite for local development and PostgreSQL for production.

## ✨ Features

- **💸 Expense Management** — Add, edit, delete, search, and filter expenses with pagination
- **💰 Income Tracking** — Track multiple income sources (Freelance, Family, Stipend, etc.)
- **🤝 Loan Tracker (Khatabook-style)** — Track who owes you and who you owe, with full transaction history and settlement
- **🎯 Budget Management** — Set monthly overall and per-category budgets with visual progress bars
- **📊 Dashboard & Analytics** — Pie charts, bar charts, summary cards, spending trends
- **🌙 Dark Mode** — Full dark mode with localStorage persistence
- **📈 Export & Reports** — Export expenses, income, loans, and summary reports to CSV
- **₹ INR** — Indian Rupee formatting throughout
- **🔒 JWT Authentication** — Single-user login protecting all API routes

## 🛠 Tech Stack

| Layer    | Technology                                |
|----------|-------------------------------------------|
| Frontend | React 18, Tailwind CSS, Recharts, Axios   |
| Backend  | Flask (Python), SQLite / PostgreSQL       |
| Testing  | pytest (backend), Jest/RTL (frontend)     |

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- pip

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/SiddhantNarel/expense-tracker
cd expense-tracker
```

### 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
python run.py
```

The API server will start at `http://localhost:5000`

### 3. Frontend setup

```bash
cd frontend
npm install
npm start
```

The app will open at `http://localhost:3000`

## 📁 Project Structure

```
expense-tracker/
├── render.yaml                # Render one-click deployment blueprint
├── backend/
│   ├── requirements.txt
│   ├── run.py
│   ├── config.py
│   ├── hash_password.py       # Helper to generate ADMIN_PASSWORD_HASH
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── database.py        # DB connection (SQLite + PostgreSQL)
│   │   ├── routes/            # API route handlers (JWT-protected)
│   │   └── utils/             # Input validators
│   └── tests/                 # pytest tests
└── frontend/
    ├── package.json
    ├── tailwind.config.js
    └── src/
        ├── App.js
        ├── pages/Login.js     # Login page
        ├── context/ThemeContext.js
        ├── components/        # All React components
        └── services/          # API service (with JWT interceptors)
```

## 🔌 API Documentation

All endpoints (except `/api/auth/login`) require a JWT `Authorization: Bearer <token>` header.

### Auth
| Method | Endpoint            | Description                |
|--------|---------------------|----------------------------|
| POST   | `/api/auth/login`   | Login, returns JWT token   |
| GET    | `/api/auth/verify`  | Verify token validity      |

### Expenses
| Method | Endpoint               | Description                  |
|--------|------------------------|------------------------------|
| GET    | `/api/expenses`        | List with filters/pagination |
| GET    | `/api/expenses/<id>`   | Get single expense           |
| POST   | `/api/expenses`        | Create expense               |
| PUT    | `/api/expenses/<id>`   | Update expense               |
| DELETE | `/api/expenses/<id>`   | Delete expense               |

### Income
| Method | Endpoint             | Description          |
|--------|----------------------|----------------------|
| GET    | `/api/income`        | List income          |
| POST   | `/api/income`        | Add income           |
| PUT    | `/api/income/<id>`   | Update income        |
| DELETE | `/api/income/<id>`   | Delete income        |

### Loans (Khatabook)
| Method | Endpoint                           | Description              |
|--------|------------------------------------|--------------------------|
| GET    | `/api/friends`                     | List friends + balances  |
| POST   | `/api/friends`                     | Add friend               |
| PUT    | `/api/friends/<id>`                | Update friend            |
| DELETE | `/api/friends/<id>`                | Delete friend            |
| GET    | `/api/friends/<id>/transactions`   | Transaction history      |
| POST   | `/api/friends/<id>/transactions`   | Add gave/received entry  |
| POST   | `/api/friends/<id>/settle`         | Settle balance           |

### Budgets
| Method | Endpoint             | Description         |
|--------|----------------------|---------------------|
| GET    | `/api/budgets`       | List budgets        |
| POST   | `/api/budgets`       | Set/update budget   |
| DELETE | `/api/budgets/<id>`  | Delete budget       |

### Analytics
| Method | Endpoint                             | Description             |
|--------|--------------------------------------|-------------------------|
| GET    | `/api/analytics/summary`             | Dashboard summary       |
| GET    | `/api/analytics/category-breakdown`  | Spending by category    |
| GET    | `/api/analytics/trends`              | Daily/weekly/monthly    |
| GET    | `/api/analytics/income-vs-expense`   | Income vs expense       |

### Export
| Method | Endpoint                 | Description           |
|--------|--------------------------|-----------------------|
| GET    | `/api/export/expenses`   | CSV export expenses   |
| GET    | `/api/export/income`     | CSV export income     |
| GET    | `/api/export/loans`      | CSV export loans      |
| GET    | `/api/export/report`     | Full summary report   |

## 🧪 Testing

### Backend

```bash
cd backend
pytest tests/ -v
```

### Frontend

```bash
cd frontend
npm test
```

## 🗄 Database Schema

| Table               | Key Columns                                                          |
|---------------------|----------------------------------------------------------------------|
| `expenses`          | id, amount, category_id, date, description, payment_method          |
| `income`            | id, amount, source, date, description                                |
| `categories`        | id, name, emoji, color, is_custom                                    |
| `friends`           | id, name, phone, notes                                               |
| `loan_transactions` | id, friend_id, type (gave/received/settlement), amount, date        |
| `budgets`           | id, category_id, amount, month, year                                 |
| `settings`          | id, key, value                                                       |

## 🚀 Deployment on Render

This project includes a `render.yaml` blueprint for one-click deployment on [Render](https://render.com).

### Quick Deploy

1. Fork or push this repository to GitHub.
2. In the Render dashboard, select **New > Blueprint** and connect your repo.
3. Render will create the backend web service, frontend static site, and a free PostgreSQL database automatically.
4. Set the required environment variables (see below).

### Environment Variables

Set these in the Render dashboard for the **backend** service:

| Variable              | Description                                                   |
|-----------------------|---------------------------------------------------------------|
| `ADMIN_USERNAME`      | Login username (e.g. `admin`)                                 |
| `ADMIN_PASSWORD_HASH` | Hashed password — generate with `python hash_password.py`    |
| `JWT_SECRET_KEY`      | Auto-generated by Render (`generateValue: true`)              |
| `DATABASE_URL`        | Auto-populated by the Render PostgreSQL add-on                |
| `FRONTEND_URL`        | URL of your deployed frontend (for CORS, e.g. `https://expense-tracker-frontend.onrender.com`) |

For the **frontend** static site:

| Variable              | Description                                                   |
|-----------------------|---------------------------------------------------------------|
| `REACT_APP_API_URL`   | Full URL of the backend API (e.g. `https://expense-tracker-backend.onrender.com/api`) |

### Generating a Password Hash

```bash
cd backend
python hash_password.py mysecretpassword
```

Copy the output and paste it as the value of `ADMIN_PASSWORD_HASH` in Render.

### Local Development

Local development continues to use SQLite — no changes needed. Simply run the backend without a `DATABASE_URL` environment variable and it will fall back to SQLite automatically.

## 🔮 Future Enhancements

- Recurring expense templates
- Push notifications for budget alerts
- Mobile app (React Native)
- Bank statement import (CSV/PDF)
