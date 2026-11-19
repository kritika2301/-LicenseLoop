# LicenseLoop – Software License & Renewal Management System

LicenseLoop is a web-based software license management system designed to help organizations manage software licenses, vendors, license expenses, and renewal schedules from one centralized dashboard.

The application provides an organized way to monitor license information, track expiry dates, and generate reports.

## Features

- **Dashboard:** View software statistics, license summaries, expenditure, and recent license activity.
- **Software Management:** Add, view, edit, delete, search, and filter software records.
- **Vendor Management:** Maintain vendor information and manage vendor records.
- **License Management:** Create, update, view, delete, search, and filter software licenses.
- **Renewal Tracking:** Monitor upcoming expirations, view renewal reminders, and update license statuses.
- **Reports:** View license summaries, renewal reports, software expenditure, and export reports as CSV files.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Database | PostgreSQL |
| Database Connectivity | Psycopg |
| Templates | Jinja2 |
| Charts | Chart.js |
| Version Control | Git and GitHub |

## Project Structure

```text
LicenseLoop/
│
├── app/
│   ├── __init__.py
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

Activate it on Windows:

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
```

Use your own PostgreSQL password. Do not upload the `.env` file to GitHub.

### 6. Run the application

```bash
python run.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## Database

LicenseLoop uses PostgreSQL to store:

- User records
- Vendor details
- Software information
- Software license records

## Future Enhancements

- User authentication and role-based access.
- Automated email renewal notifications.
- Cloud deployment.
- Advanced analytics and reporting.

## Author

**Kritika Manchekar**

MSc Computer Science Student

GitHub: [kritika2301](https://github.com/kritika2301)

---

*LicenseLoop – Simplifying Software License and Renewal Management.*