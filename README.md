# 🎵 Tour Event Alert — Web Scraper & Email Notifier

A lightweight Python automation tool that monitors a live music tour listing page, detects new events, stores them in a local SQLite database, and instantly sends an email notification whenever a new tour is found.

---

## 📌 Features

- 🔍 **Web Scraping** — Continuously scrapes a target URL for upcoming tour events using CSS selectors
- 🗄️ **Database Storage** — Persists discovered events in a local SQLite database to avoid duplicate alerts
- 📧 **Email Notifications** — Sends an automatic Gmail alert the moment a new event is detected
- ⚙️ **Environment-based Config** — Sensitive credentials are managed securely via a `.env` file
- 🔁 **Continuous Polling** — Runs in a loop, checking for updates every 2 seconds

---

## 🗂️ Project Structure

```
web_scraping/
├── main.py            # Core application logic (scraper, emailer, database)
├── extract.yaml       # CSS selector configuration for data extraction
├── data.db            # SQLite database storing logged events
├── .env.example       # Template for environment variable configuration
└── .gitignore         # Files excluded from version control
```

---

## ⚙️ How It Works

```
┌─────────────────────┐
│  Scrape Target URL  │  ← requests + custom User-Agent header
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Extract Tour Data  │  ← selectorlib parses HTML via extract.yaml CSS selector
└────────┬────────────┘
         │
         ▼
┌──────────────────────────┐
│  Is it "No upcoming      │──── Yes ──→ Sleep 2s → Repeat
│  tours"?                 │
└────────┬─────────────────┘
         │ No
         ▼
┌──────────────────────────┐
│  Check Database          │──── Already exists ──→ Sleep 2s → Repeat
│  (band, city, date)      │
└────────┬─────────────────┘
         │ New event
         ▼
┌──────────────────────────┐
│  Store in data.db        │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Send Email Alert        │  ← Gmail SMTP over SSL (port 465)
└──────────────────────────┘
```

---

## 🔐 Environment Variables

Credentials are never hardcoded. The app reads them from a `.env` file at runtime using `python-dotenv`.

### Setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and fill in your credentials:
   ```env
   MY_GMAIL_PASSWORD=your_gmail_app_password
   SENDER_MAIL=your_email@gmail.com
   RECEIVER_MAIL=recipient_email@gmail.com
   ```

> **⚠️ Important:** Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your regular account password. Regular passwords will not work if 2-Step Verification is enabled.

The `.env` file is listed in `.gitignore` and will **never** be committed to version control.

---

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- A Gmail account with an App Password enabled

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/web-scraping-tour-alert.git
cd web-scraping-tour-alert

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install requests selectorlib python-dotenv

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your Gmail credentials

# 5. Run the application
python main.py
```

---

## 📦 Dependencies

| Package          | Purpose                                      |
|------------------|----------------------------------------------|
| `requests`       | Fetches page HTML from the target URL        |
| `selectorlib`    | Extracts data from HTML using CSS selectors  |
| `python-dotenv`  | Loads credentials from the `.env` file       |
| `smtplib` / `ssl`| Sends email via Gmail SMTP (stdlib)          |
| `sqlite3`        | Local database for deduplication (stdlib)    |

---

## 🧩 CSS Selector Configuration

The `extract.yaml` file defines which HTML element contains tour data:

```yaml
tours:
  css: '#displaytimer'
```

To scrape a different page, update the `URL` in `main.py` and adjust the CSS selector in `extract.yaml` to match the target element.

---

## 📧 Email Alert Format

When a new event is detected, an email is sent with the following format:

```
Subject: EVENT ALERT!

Hey, new event was found!
```

---

## 🔒 Security Notes

- Never commit your `.env` file — it is already excluded via `.gitignore`
- Always use Gmail **App Passwords** instead of your main account password
- The `.env.example` file serves as a safe, credential-free reference for collaborators

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
