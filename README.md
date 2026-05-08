# 📱 WageWise Monthly Survey Bot

> **A multi-stage WhatsApp survey bot for the ASISA Foundation's WageWise financial-literacy programme — registers participants, runs a 15-question baseline, then drives a recurring 3-question monthly survey with automatic airtime rewards.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2.3-000000?logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)](https://www.sqlalchemy.org/)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp_+_SMS-F22F46?logo=twilio&logoColor=white)](https://www.twilio.com/)
[![Africa's Talking](https://img.shields.io/badge/Africa's_Talking-Airtime-FF6B00)](https://africastalking.com/)
[![Azure](https://img.shields.io/badge/Azure-Web_App-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![SQL Server](https://img.shields.io/badge/Azure_SQL-MSSQL-CC2927?logo=microsoftsqlserver&logoColor=white)](https://azure.microsoft.com/en-us/products/azure-sql/)
[![Deploy](https://github.com/abdullahek/wagwise-monthly/actions/workflows/main_wagewise-monthly.yml/badge.svg)](https://github.com/abdullahek/wagwise-monthly/actions/workflows/main_wagewise-monthly.yml)

---

## 🌟 Overview

**WageWise Monthly** is the long-running engagement bot for the **WageWise** financial-education programme run by **Genesis Analytics** for the **ASISA Foundation** in South Africa.

Where the *endline* bot collects a one-off 21-question final survey, this bot is the **front-end of the 3-year participant journey**:

1. **Welcomes** new participants over WhatsApp and obtains opt-in consent.
2. **Runs a 15-question baseline survey** (rewards **R75 ZAR airtime**).
3. **Registers** them for monthly check-ins.
4. **Sends a 3-question monthly survey** every month (rewards **R17 ZAR airtime**, plus an additional **R20** bonus for completing 4 months in a row).
5. **Manages airtime delivery problems** — if airtime fails to land, an OTP-based flow lets the user verify a different phone number (separate `airtime_number` from their WhatsApp `number`).
6. **Bulk re-engagement** — utilities for SMS-blasting affected users to invite them back to fix their delivery details.

---

## ✨ Core Features

### 💬 Multi-stage WhatsApp Conversation
A single Twilio webhook (`/message`) hands off to specialised view handlers depending on `session['view']`:

| View | Route | Purpose |
|------|-------|---------|
| Welcome / opt-in | `/message` (`glogic/bot_view.py`) | Initial yes/no consent + call-back consent (a/b) |
| Baseline survey | `/baseline` (`glogic/baseline_view.py`) | 15-question intake survey + R75 airtime |
| Monthly survey | `/survey` (`glogic/survey_view.py`) | 3-question monthly survey + R17 airtime |
| Phone verification | `/correct_number`, `/get_new_number`, `/otp` | OTP flow when the airtime number differs from WhatsApp number |

### 📋 JSON-driven Survey Definitions
- `dbseeding/registration.json` — 27 demographic registration questions
- `dbseeding/baseline.json` — 15 baseline financial-literacy questions
- `dbseeding/monthly.json` — Recurring monthly mood/finance check-ins
- Seeded into MSSQL via `python manage.py dbseed` (uses `glogic/parser.py`)

### 🧠 Smart Survey Logic
- **Skip logic** — questions 3 and 5 of the baseline conditionally skip the next question if answer ≠ `3`
- **Single-vs-multi-select validation** — rejects multi-answers on questions tagged single-select
- **Range validation** — answers checked against `num_ops` per question
- **Quarterly rotation** — monthly questions rotate through 3 sets (`(month % 3) → 1, 4, or 7`) so participants get fresh questions each quarter
- **Per-user resume** — `session['question_id']` + `session['count']` track progress

### 🎁 Automated Airtime Rewards (Africa's Talking)
- **R75 ZAR** on baseline completion
- **R17 ZAR** per monthly survey
- Sent via the Africa's Talking Airtime API to each user's verified `airtime_number`
- Bulk retrospective sender (`send_many_retrospective`) for back-pay runs from an Excel sheet

### 📲 OTP-based Phone Verification
For users whose WhatsApp number differs from the SIM that should receive the airtime:
1. User says "no" when asked to confirm their current number
2. Bot collects a new SA-formatted number (`^0\d{9}$`) → `get_new_number_view.py`
3. Twilio SMS dispatches a 5-digit OTP → `otp_view.py`
4. User echoes the OTP back in WhatsApp; on match, `users.airtime_number` is updated

### 📨 Bulk SMS Re-engagement (`bulk_sending/`)
- `template_send.py` — Twilio-driven outbound WhatsApp invites to users in `airtime_correction_numbers`
- `bulk_send.py` — Africa's Talking SMS class for pulling the correction list and re-inviting them
- `sql_stuff.py` — Helper queries (`validate_num`, `update_response`, `del_from_db`, `get_data_ud`)

### ☁️ Production Deployment
- **Azure Web App** (`wagewise-monthly`) — auto-deploy on push to `main`
- **Gunicorn** with a 600-second timeout
- `startup.sh` installs `unixodbc-dev` + `msodbcsql17` on container boot

---

## 🏗️ Architecture

```
                    ┌────────────────────────┐
                    │      Participant       │
                    │   (WhatsApp on phone)  │
                    └──────────┬─────────────┘
                               │
                               ▼
                    ┌────────────────────────┐
                    │        Twilio          │
                    │  WhatsApp + SMS APIs   │
                    └──────────┬─────────────┘
                               │ POST /message (or /baseline /survey /otp ...)
                               ▼
       ┌────────────────────────────────────────────────────┐
       │           Flask App (Azure Web App)                │
       │                                                    │
       │   ┌─────────────────────────────────────────────┐  │
       │   │           views.py (router)                 │  │
       │   └────┬────────┬───────────┬───────────┬───────┘  │
       │        ▼        ▼           ▼           ▼          │
       │  ┌──────────┐┌──────────┐┌──────────┐┌──────────┐  │
       │  │ bot_view ││ baseline ││ survey   ││  otp /   │  │
       │  │  (opt-in)││ (R75)    ││ (R17 mo) ││ correct  │  │
       │  └────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘  │
       │       │           │           │           │        │
       │       ▼           ▼           ▼           ▼        │
       │  ┌──────────────────────────────────────────────┐  │
       │  │ models.py (SQLAlchemy)  +  send_airtime.py   │  │
       │  │ parser.py  +  bulk_sending/*                 │  │
       │  └──────────┬───────────────────────────┬───────┘  │
       └─────────────┼───────────────────────────┼──────────┘
                     ▼                           ▼
            ┌──────────────────┐       ┌──────────────────┐
            │  Azure SQL DB    │       │ Africa's Talking │
            │  (MSSQL)         │       │  Airtime API     │
            │ ─ users          │       │  (R17 / R75 ZAR) │
            │ ─ baseline_*     │       └──────────────────┘
            │ ─ monthly_*      │
            │ ─ responses      │
            │ ─ Campaign_*     │
            └──────────────────┘
```

---

## 📦 Project Structure

```
wagwise-monthly/
├── .github/
│   └── workflows/
│       └── main_wagewise-monthly.yml    # CI/CD → Azure Web App
├── glogic/                              # Flask application package
│   ├── __init__.py                      # App + DB factory (prepare_app)
│   ├── config.py                        # MSSQL & Test config (env-driven)
│   ├── models.py                        # SQLAlchemy ORM (users + answers + responses)
│   ├── views.py                         # Root + view-module loader
│   ├── bot_view.py                      # /message — initial opt-in flow
│   ├── baseline_view.py                 # /baseline — 15Q intake survey + R75
│   ├── survey_view.py                   # /survey — monthly 3Q survey + R17
│   ├── otp_view.py                      # /otp — OTP verification
│   ├── correct_number_view.py           # /correct_number — confirm SIM number
│   ├── get_new_number_view.py           # /get_new_number — capture new SA number
│   ├── gresponses.py                    # Welcome / consent message dictionary
│   ├── parser.py                        # JSON → DB seed parser
│   ├── send_airtime.py                  # Africa's Talking airtime SDK wrapper
│   ├── utils.py                         # Misc Twilio helpers
│   └── validation_test.py               # Phone-number lookup against user_demographics
├── bulk_sending/
│   ├── bulk_send.py                     # SMS class for re-engagement campaigns
│   ├── template_send.py                 # Twilio WhatsApp template + airtime list ops
│   └── sql_stuff.py                     # Raw-SQL helpers (validate_num, etc.)
├── dbseeding/
│   ├── registration.json                # 27 demographic questions
│   ├── baseline.json                    # 15 baseline finance questions
│   └── monthly.json                     # Recurring monthly questions
├── migrations/                          # Alembic / Flask-Migrate
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
├── manage.py                            # Flask CLI entrypoint (dbseed)
├── startup.sh                           # Azure container boot (gunicorn)
├── requirements.txt
└── README.md
```

---

## 🗃️ Database Schema

### SQLAlchemy ORM (`glogic/models.py`)

| Table | Key columns | Purpose |
|-------|-------------|---------|
| `users` | `id`, `number`, `number_2`, `airtime_number`, `registered`, `last_month_completed` | Participant master record |
| `baseline_questions` | `id`, `content`, `num_ops` | Seeded 15-question baseline bank |
| `monthly_questions` | `id`, `content`, `num_ops` | Seeded monthly question bank (rotating) |
| `baseline_answers` | `content`, `question_id`, `user_id` | Per-user baseline responses |
| `monthly_answers` | `content`, `question_id`, `user_id`, `month`, `date` | Per-user monthly responses, stamped with computed month index |
| `responses` | `number`, `month`, `question_1..3`, `date_completed` | Compact monthly-response summary |

### Auxiliary MSSQL tables (used directly via `pyodbc`)
| Table | Used by |
|-------|---------|
| `user_demographics` | `validation_test.py`, `bulk_sending/sql_stuff.py` (lookup name + number) |
| `airtime_correction_numbers` | `bulk_sending/template_send.py` (re-engagement queue) |
| `Campaign_Responses` | `bulk_sending/sql_stuff.py` (`validate_num`, `update_response`) |

> **Month index convention:** `month = (year - 2022) * 12 + (month - 8)` — i.e. month `1` is **September 2022** (programme start). All progress checks use this integer.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| Web framework | Flask 2.2.3 (with `FlaskGroup` CLI) |
| WSGI server | Gunicorn 20 (production) / Flask dev server (local) |
| ORM / Migrations | SQLAlchemy 2.0 + Flask-Migrate (Alembic) |
| Raw SQL driver | pyodbc 4 (ODBC Driver 18 for SQL Server) |
| Database | Azure SQL (MSSQL) |
| Messaging | Twilio WhatsApp + Twilio SMS (OTP) |
| Airtime rewards | Africa's Talking (Python SDK 1.2.4) |
| Data utilities | pandas 1.3.5, numpy 1.21.6, openpyxl |
| Hosting | Azure App Service (Linux) |
| CI/CD | GitHub Actions → Azure publish-profile deploy |

---

## 🛠️ Local Development

### Prerequisites
- Python **3.8+**
- ODBC Driver 18 for SQL Server ([Microsoft download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server))
- Azure SQL instance (or use the bundled `TestConfig` SQLite mode)
- Twilio account + WhatsApp sandbox number + SMS-enabled number
- Africa's Talking sandbox account
- `ngrok` to expose your local server to Twilio

### 1. Clone & install

```bash
git clone https://github.com/abdullahek/wagwise-monthly.git
cd wagwise-monthly

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file (do **not** commit it):

```bash
SECRET_KEY=change-me
DEBUG=True

# Azure SQL (used by glogic/config.py and bulk_sending/*)
SERVER=your-server.database.windows.net
DATABASE=your-db
NAME=your-username
PASSWORD=your-password

# Twilio (used by otp_view, correct_number_view, get_new_number_view, template_send)
TWILIO_ACCOUNT_SID=ACxxxx
TWILIO_AUTH_TOKEN=your-auth-token

# Africa's Talking — currently hardcoded in send_airtime.py / bulk_send.py
# Move to env vars before any production hardening:
# AT_USERNAME=...
# AT_API_KEY=...
```

Source it:

```bash
set -a; source .env; set +a
```

### 3. Run migrations & seed the DB

```bash
flask --app manage db upgrade        # apply schema
python manage.py dbseed              # load registration/baseline/monthly JSONs
```

> The `dbseed` command in `manage.py` currently only seeds **monthly** questions by default. Uncomment the registration / baseline blocks in `manage.py` to seed those as well.

### 4. Run the bot

**Flask dev server:**
```bash
flask --app manage run -p 5000
```

**Gunicorn (production-like):**
```bash
gunicorn --bind=0.0.0.0 --timeout 600 manage:app
```

### 5. Expose to Twilio

```bash
ngrok http 5000
```

Configure your Twilio WhatsApp Sandbox webhook → `https://<ngrok-id>.ngrok.io/message`.

---

## 🔄 Participant Journey

```
                  New participant sends "Hi"
                            │
                            ▼
            ┌───────────────────────────────┐
            │  Welcome (gresponses.py)      │
            │  → consent prompt 1/2 (Yes/No)│
            └───────────────┬───────────────┘
                            │ Yes
                            ▼
            ┌───────────────────────────────┐
            │  /baseline  (15 questions)    │
            │   ─ skip logic on Q3, Q5      │
            │   ─ multi-select on Q8, Q14   │
            └───────────────┬───────────────┘
                            │ on completion
                            ▼
            ┌───────────────────────────────┐
            │  user.registered = 1          │
            │  send_airtime  R75 ZAR        │
            └───────────────┬───────────────┘
                            │
                            ▼
                  ◀───── monthly cycle ─────▶
                            │
                            ▼
            ┌───────────────────────────────┐
            │  /survey  (3 questions)       │
            │   ─ rotates via month % 3     │
            │   ─ session['count'] enforces │
            │     stop at 3                 │
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ user.last_month_completed =   │
            │   current_month               │
            │ send_airtime  R17 ZAR         │
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  Airtime not received?        │
            │   → /correct_number → OTP →   │
            │     update users.airtime_     │
            │     number                    │
            └───────────────────────────────┘
```

---

## 🌐 API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` / `POST` | `/` | Health check — returns *"I'm working"* |
| `GET` / `POST` | `/message` | Initial WhatsApp webhook (opt-in / call-consent) |
| `GET` / `POST` | `/baseline` | 15-question baseline survey + R75 airtime |
| `GET` / `POST` | `/survey` | 3-question monthly survey + R17 airtime |
| `GET` / `POST` | `/correct_number` | "Is `0xxxxxx` the right number?" yes/no flow |
| `GET` / `POST` | `/get_new_number` | Collect a new SA-formatted number |
| `GET` / `POST` | `/otp` | Validate the SMS-delivered OTP |

---

## 🚢 Deployment (Azure)

1. **GitHub Actions** (`.github/workflows/main_wagewise-monthly.yml`)
   - Builds with Python 3.8
   - Installs dependencies
   - Uploads the artifact and deploys to App Service `wagewise-monthly` (Production slot)
   - Uses `AZUREAPPSERVICE_PUBLISHPROFILE_*` repository secret
2. **Container start** (`startup.sh`)
   - Installs `unixodbc-dev` + `msodbcsql17` (required by `pyodbc`)
   - Boots gunicorn with a 600s timeout
3. **Twilio webhook** → `https://wagewise-monthly.azurewebsites.net/message`

### Required Azure / GitHub secrets

| Secret | Used by |
|--------|---------|
| `AZUREAPPSERVICE_PUBLISHPROFILE_*` | GitHub Actions deploy |
| `SERVER`, `DATABASE`, `NAME`, `PASSWORD` | App settings (Azure SQL) |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | OTP SMS + bulk template send |
| `SECRET_KEY`, `DEBUG` | Flask config |

---

## 🔒 Security & Tech-Debt Notes

The repo is functional but inherits several patterns from the original G:Bot template that should be hardened before further production use:

- 🔴 **Hardcoded Africa's Talking API key** — `glogic/send_airtime.py` and `bulk_sending/bulk_send.py` both ship a real-looking key in source. Move to env vars / Azure Key Vault and rotate immediately.
- 🔴 **F-string SQL** — `bulk_sending/sql_stuff.py`, `validation_test.py`, `bulk_sending/template_send.py` all build queries with string interpolation. Replace with parameterised queries.
- 🟠 **Twilio request signature** is not validated — any anonymous POST to `/message` is accepted.
- 🟠 **Session secret in env var only** — fine for Azure App Settings but `SECRET_KEY` must never be unset (no fallback) before going live.
- 🟠 **`bulk_send.py` uses an undefined `pyodbc`** — the import is missing; the script will crash if run as-is.
- 🟠 **Duplicate connection boilerplate** — every `bulk_sending/*` function rebuilds the MSSQL connection string. Centralise into a shared helper.
- 🟢 **Dead code** — `glogic/utils.py::return_to_menu` references `Dictionary['welcome']` which no longer exists in `gresponses.py`.

---

## 🧪 Useful Commands

```bash
# Apply DB migrations
flask --app manage db upgrade

# Seed monthly questions (uncomment baseline / registration in manage.py to seed those)
python manage.py dbseed

# Send airtime to a back-list of recipients (Excel sheet input)
python -m glogic.send_airtime

# Run the re-engagement WhatsApp blast for users in airtime_correction_numbers
python -m bulk_sending.template_send
```

---

## 📄 License

This project is private and proprietary to its owner. All rights reserved.

---

## 👤 Author / Maintainer

**Abdullah EK** — [@abdullahek](https://github.com/abdullahek)

> Originally based on the **G:Bot** template by Genesis Analytics, adapted for the **WageWise** programme monthly engagement loop.

---

<p align="center">
  Built with ❤️ for long-running financial-literacy research at scale
</p>
