# AI-Powered Customer Support & Ticket Management System

A web-based customer support application built with Python, Flask, and MySQL. It allows users to submit support tickets and receive AI-generated responses, with ticket details and responses stored in a database.

## Features

* Submit support tickets through a web interface.
* Categorize tickets and assign priorities.
* Store user and ticket information in MySQL.
* Generate and display AI-powered support responses.
* Save AI responses to the database.
* Provide a backend health-check endpoint.

## Technology Stack

* **Backend:** Python, Flask
* **Database:** MySQL
* **Frontend:** HTML, CSS, JavaScript
* **AI integration:** Python AI service
* **Version control:** Git and GitHub

## Project Structure

```text
AI Customer Support Project/
├── app.py
├── ai_service.py
├── services/
│   └── ai_service.py
├── databse/
│   └── schema.sql
├── static/
│   └── js/
│       ├── css/
│       │   └── style.css
│       └── script.js
├── templates/
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   └── ticket.html
├── test_ai.py
├── test_db.py
├── test_local_ai.py
├── test_register.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

* Python 3.11
* MySQL Server
* Git

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "AI Customer Support Project"
```

Replace the example repository URL and folder name with the actual values.

### 2. Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the Database

Start MySQL Server and create the database:

```sql
CREATE DATABASE customer_support;
```

Run the database schema in `databse/schema.sql` to create the required tables and indexes.

### 5. Configure Environment Variables

Create a local `.env` file in the project root. Configure the database credentials and other settings required by the application.

Example database settings:

```text
DB_HOST=127.0.0.1
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=customer_support
```

Replace the example username and password with your own local MySQL credentials. Configure any additional AI-service settings required by the application.

**Security:** Never commit `.env`, API keys, passwords, or other sensitive credentials to GitHub.

### 6. Run the Application

```powershell
python app.py
```

Open the application:

`http://127.0.0.1:5000/`

Check the backend health endpoint:

`http://127.0.0.1:5000/health`

## Testing

The project includes test scripts for AI integration, database connectivity, local AI, and user registration.

Run the relevant tests after configuring the database and AI service.

## Current Project Status

The application has been tested locally for:

* Ticket submission
* Database storage and retrieval
* AI-response display and persistence
* Backend health-check response

Further security testing, GitHub publication, and online deployment remain to be completed.

## Future Improvements

* Improve ticket tracking and management.
* Strengthen authentication and authorization.
* Add comprehensive input validation and error handling.
* Improve the interface and accessibility.
* Deploy the application online.

## Author

Developed as a portfolio project demonstrating practical skills in Python, Flask, MySQL, frontend development, and AI integration.
