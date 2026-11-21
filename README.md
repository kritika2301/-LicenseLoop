# LicenseLoop – Software License & Renewal Management System

LicenseLoop is a web-based software license management system designed to help organizations manage software licenses, vendors, license expenses, and renewal schedules from one centralized dashboard.

The application provides an organized way to monitor license information, track expiry dates, manage renewals, and generate reports.

## Features

- **Dashboard:** View software statistics, license summaries, expenditure, and recent license activity.
- **Software Management:** Add, view, edit, delete, search, and filter software records.
- **Vendor Management:** Maintain vendor information and manage vendor records.
- **License Management:** Create, update, view, delete, search, and filter software licenses.
- **Renewal Tracking:** Monitor upcoming expirations, view renewal reminders, and update license statuses.
- **Reports:** View license summaries, renewal reports, software expenditure, and export reports as CSV files.
- **Admin Authentication:** Secure admin login and logout functionality.
- **Password Security:** Store passwords using secure password hashing.
- **Session Management:** Restrict application access to authenticated users.
- **CSRF Protection:** Protect form submissions against Cross-Site Request Forgery attacks.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Database | PostgreSQL |
| Database Connectivity | Psycopg |
| Templates | Jinja2 |
| Charts | Chart.js |
| Authentication & Security | Werkzeug Security, Flask-WTF |
| Environment Configuration | python-dotenv |
| Version Control | Git and GitHub |

## Project Structure

```text
LicenseLoop/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── db.py
│   └── routes.py
│
├── database/
│   ├── schema.sql
│   └── sample_data.sql
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── software.html
│   ├── edit_software.html
│   ├── vendors.html
│   ├── edit_vendor.html
│   ├── licenses.html
│   ├── edit_license.html
│   ├── renewals.html
│   └── reports.html
│
├── config.py
├── run.py
├── requirements.txt
├── .env
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/kritika2301/-LicenseLoop.git
cd -LicenseLoop
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

- Install and start PostgreSQL.
- Create a database named `licenseloop_db`.
- Execute `database/schema.sql` to create the required tables.
- Execute `database/sample_data.sql` to insert sample records.

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DB_PASSWORD=your_postgresql_password
SECRET_KEY=your_generated_secret_key
```

Generate a secure Flask secret key using:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into `SECRET_KEY`.

**Important:** Replace the database password with your own PostgreSQL password. Never upload your `.env` file or secret key to GitHub.

### 6. Run the application

```bash
python run.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

You will be redirected to the Admin Login page if you are not authenticated.

Use the Admin account configured in the database to log in.

## Database

LicenseLoop uses PostgreSQL to store:

- User records and authentication details
- Vendor information
- Software information
- Software license records

## Security

LicenseLoop includes the following security measures:

- Password hashing using Werkzeug.
- Session-based authentication.
- Protected application routes.
- CSRF protection using Flask-WTF.
- Environment variables for sensitive configuration.
- Git exclusions for
