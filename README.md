# Student Management System

A web-based Student Management System built with **FastAPI**, **Jinja2**, and **HTML/CSS**. It provides separate student and administrator portals for viewing and managing student records.

## Features

## ⚙️ Built With

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat-square)
![PyJWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens)
![JSON](https://img.shields.io/badge/Storage-JSON-lightgrey?style=flat-square)

### Student Portal
- Student login using registered name and roll number.
- JWT-based authentication using HTTP-only cookies.
- Personal dashboard displaying student information.
- Access restricted to the authenticated student's record.

# Student Management System

A web-based Student Management System built with FastAPI, Jinja2, and HTML/CSS.

## 🛠️ Technologies Used

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,html,css,git,github" />
</p>
### Admin Portal
- Separate administrator login.
- Dashboard displaying registered student records and total student count.
- Register new students.
- Update existing student information.
- Delete student records with a confirmation step.

### Technical Features
- FastAPI backend and routing.
- Jinja2 server-side HTML templates.
- JWT authentication with PyJWT.
- JSON-based student data storage.
- Environment configuration using `python-dotenv`.
- Static file support.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | Web framework |
| Jinja2 | HTML templating |
| HTML & CSS | User interface |
| PyJWT | Authentication tokens |
| JSON | Student data storage |
| python-dotenv | Environment configuration |

## Project Structure

```text
student-management-fastapi/
│
├── main.py
├── models.py
├── requirements.txt
├── students.json
├── .env
│
├── static/
│
└── templates/
    ├── home.html
    ├── login.html
    ├── students.html
    ├── admin_login.html
    └── admin_dashboard.html
```

`students.json` and `.env` should be created locally if they are not already present.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/HafizHassanAlee/student-management-fastapi.git
cd student-management-fastapi
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
SECRET_KEY_ENV=your_long_random_secret_key
ALGORITHM_ENV=HS256
ACCESS_TOKEN_EXPIRE_MINUTES_ENV=30

ADMIN_USERNAME=admin
ADMIN_PASSWORD=change_this_password
```

Use your own strong secret key and administrator password. Never upload your `.env` file to GitHub.

### 5. Create student data

Create `students.json` in the project root.

Example:

```json
{
    "3520112345678": {
        "name": "Ali Khan",
        "age": 20,
        "gender": "Male",
        "city": "Lahore",
        "roll no": "Stf-501",
        "major": "Computer Science",
        "gpa": 3.7
    }
}
```

The CNIC is used as the top-level record key.

**Student login credentials:** The current implementation uses the student's name as the username and roll number as the password.

### 6. Run the application

```bash
fastapi dev main.py
```

Alternatively:

```bash
uvicorn main:app --reload
```

Open:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Application Routes

| Route | Description |
|---|---|
| `/` | Home page and portal selection |
| `/login` | Student login |
| `/dashboard` | Student dashboard |
| `/admin/login` | Admin login |
| `/admin/dashboard` | Admin dashboard |
| `/admin/students/create` | Register a student |
| `/admin/students/update` | Update student information |
| `/admin/students/delete` | Delete a student |

## Student Information

Each student record contains:

- CNIC
- Name
- Age
- Gender
- City
- Roll Number
- Major / Department
- GPA

## Future Improvements

- PostgreSQL database integration.
- SQLAlchemy ORM.
- Individual student passwords with secure password hashing.
- Improved authentication and authorization.
- Logout functionality.
- Stronger server-side validation.
- Automated testing.

## Development Notes

This is a learning project. The current implementation uses JSON-file storage rather than a relational database. Before production use, admin-only route protection, password handling, cookie security, and input validation should be strengthened.

The update route also needs an `HTMLResponse` import in `main.py` for its error-handling responses.

## Author

**Hassan Ali**

GitHub: [@HafizHassanAlee](https://github.com/HafizHassanAlee)

---

If you find this project useful, consider giving the repository a ⭐.
