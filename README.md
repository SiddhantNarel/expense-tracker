# 💰 Personal Expense Tracker

A full-stack **Personal Finance Tracker** with React frontend and Flask backend, using SQLite for zero-setup portability.

## ✨ Features

- **💸 Expense Management** — Add, edit, delete, search, and filter expenses with pagination
- **💰 Income Tracking** — Track multiple income sources (Freelance, Family, Stipend, etc.)
- **🤝 Loan Tracker (Khatabook-style)** — Track who owes you and who you owe, with full transaction history and settlement
- **🎯 Budget Management** — Set monthly overall and per-category budgets with visual progress bars
- **📊 Dashboard & Analytics** — Pie charts, bar charts, summary cards, spending trends
- **🌙 Dark Mode** — Full dark mode with localStorage persistence
- **📈 Export & Reports** — Export expenses, income, loans, and summary reports to CSV
- **₹ INR** — Indian Rupee formatting throughout

## 🛠 Tech Stack

| Layer    | Technology                                |
|----------|-------------------------------------------|
| Frontend | React 18, Tailwind CSS, Recharts, Axios   |
| Backend  | Flask (Python), SQLite                    |
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
├── backend/
│   ├── requirements.txt
│   ├── run.py
│   ├── config.py
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── database.py        # SQLite init & connection
│   │   ├── routes/            # API route handlers
│   │   └── utils/             # Input validators
│   └── tests/                 # pytest tests
└── frontend/
    ├── package.json
    ├── tailwind.config.js
    └── src/
        ├── App.js
        ├── context/ThemeContext.js
        ├── components/        # All React components
        └── services/          # API service & helpers
```

## 🔌 API Documentation

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

## 🚀 Future Enhancements

- User authentication (multi-user support)
- Recurring expense templates
- Push notifications for budget alerts
- Mobile app (React Native)
- Bank statement import (CSV/PDF)
