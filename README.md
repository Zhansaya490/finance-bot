<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">💸 Telegram Finance Bot</h3>

  <p align="center">
    Personal Financial Planner in Telegram: track your income, expenses, and get daily/weekly summaries and alerts!
    <br />
    <a href="#usage"><strong>View Demo »</strong></a>
    <br />
    <br />
    <a href="#features">Features</a>
    ·
    <a href="#installation">Installation</a>
    ·
    <a href="#usage">Usage</a>
  </p>
</div>

---

## 📌 About The Project

This Telegram bot is a financial planning assistant developed using Python and the Telegram Bot API. It helps users:
- Log income and expenses by category
- Get daily or weekly budget summaries
- Set budget limits and receive alerts

It’s perfect for students, freelancers, or anyone tracking personal finances in a simple and effective way.

---

## 🛠️ Built With

* Python 3.11
* python-telegram-bot==13.15
* APScheduler
* pandas
* openpyxl

---

## 🚀 Getting Started

### Prerequisites

Before using the bot, install the required libraries:

```bash
pip install python-telegram-bot==13.15 pandas openpyxl apscheduler
```

### Installation

1. Clone the repo or download the `.py` file
2. Replace `YOUR_TELEGRAM_BOT_TOKEN_HERE` in the code with your actual Telegram bot token
3. Run the bot:

```bash
python finance_bot_fully_fixed.py
```

---

## 💡 Usage

### Commands:

- `/start` — Welcome message
- `/help` — Command overview
- `/config` — Set income and budget categories
- `/log` — Log income or expense by category
- `/summary` — View income, expenses, and balance
- `/notifyon` — Enable daily notifications
- `/notifyoff` — Disable notifications

### Sample Notification Message:

```
📢 Ежедневная сводка:
💰 Доход: 200000₸
💸 Расходы: 75000₸
📊 Баланс: 125000₸
```

If a category limit is exceeded:
```
⚠️ Вы превысили лимит по 'транспорт': 12000₸ (лимит: 10000₸)
```

---

## 📌 File Structure

```
finance-bot/
├── finance_bot_fully_fixed.py
├── README.md
└── screenshots/          
```

---

## ✅ Features

- [x] Income and expense tracking
- [x] Daily & weekly summaries
- [x] Category breakdowns
- [x] Budget limit alerts
- [x] Fully in Telegram, no extra apps!

---

## 🤝 Authors
Zhansaya&Adil



---

<p align="right">(<a href="#readme-top">back to top</a>)</p>
