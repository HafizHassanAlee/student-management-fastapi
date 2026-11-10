from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
import json
from fastapi.staticfiles import StaticFiles
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.responses import RedirectResponse 
from fastapi import Form
from fastapi.responses import JSONResponse
import os
import hmac
from dotenv import load_dotenv

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY_ENV")
ALGORITHM = os.getenv("ALGORITHM_ENV")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES_ENV"))


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


@app.get("/")
async def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )


@app.get("/login")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )



def authenticate_student(username: str, password: str):
    with open("students.json", "r") as file:
        students = json.load(file)
    for student in students.values():
        if (
            student["name"].lower() == username.lower()
            and student["roll no"] == password
        ):
            return student
    return None


def authenticate_admin(username: str, password: str):

    if (
        hmac.compare_digest(username, ADMIN_USERNAME)
        and hmac.compare_digest(password, ADMIN_PASSWORD)
    ):
        return True

    return False



def get_current_student(request: Request):

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    payload = verify_token(token)

    roll_no = payload.get("sub")

    if not roll_no:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    with open("students.json", "r") as file:
        students = json.load(file)

    for student in students.values():

        if student["roll no"] == roll_no:
            return student

    raise HTTPException(
        status_code=401,
        detail="Student not found"
    )


def get_current_admin(request: Request):

    token = request.cookies.get("admin_access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Admin login required"
        )

    payload = verify_token(token)

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return payload


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def load_students():
    with open("students.json", "r") as file:
        return json.load(file)


def save_students(students):
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)


@app.get("/dashboard")
def dashboard(
    request: Request,
    student: dict = Depends(get_current_student)
):
    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={"student": student}
    )

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):

    student = authenticate_student(username, password)

    if not student:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    access_token = create_access_token({
        "sub": student["roll no"],
        "name": student["name"]
    })

    response = RedirectResponse(
        url="/dashboard",
        status_code=303
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        samesite="lax",
        secure=False
    )

    return response

@app.get("/admin/login")
def admin_login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={}
    )


@app.post("/admin/login")
def admin_login(
    username: str = Form(...),
    password: str = Form(...)
):

    admin = authenticate_admin(username, password)

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Incorrect admin credentials"
        )

    access_token = create_access_token({
        "sub": ADMIN_USERNAME,
        "role": "admin"
    })

    response = RedirectResponse(
        url="/admin/dashboard",
        status_code=303
    )

    response.set_cookie(
        key="admin_access_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        samesite="lax",
        secure=False
    )

    return response


@app.get("/admin/dashboard")
def admin_dashboard(
    request: Request,
    admin: dict = Depends(get_current_admin)
):

    with open("students.json", "r") as file:
        students_data = json.load(file)

    students = []

    for cnic, student in students_data.items():
        
        students.append({
        "cnic": cnic,
        "name": student["name"],
        "age": student["age"],
        "gender": student["gender"],
        "city": student["city"],
        "roll_no": student["roll no"],
        "major": student["major"],
        "gpa": student["gpa"]
    })

    total_students = len(students)

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "students": students,
            "total_students": total_students
        }
    )


@app.post("/admin/students/create")
def create_student(
    cnic: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    city: str = Form(...),
    roll_no: str = Form(...),
    major: str = Form(...),
    gpa: float = Form(...),
    admin: dict = Depends(get_current_admin)
):

    students = load_students()

    if cnic in students:
        raise HTTPException(
            status_code=400,
            detail="Student already exists"
        )

    students[cnic] = {
        "name": name,
        "age": age,
        "gender": gender,
        "city": city,
        "roll no": roll_no,
        "major": major,
        "gpa": gpa
    }

    save_students(students)

    return RedirectResponse(
        url="/admin/dashboard",
        status_code=303
    )

@app.post("/admin/students/delete")
def delete_student(
    idtodelete: str = Form(...),
    rolltodelete: str = Form(...),
    confirm_delete: str = Form(...),
    admin: dict = Depends(get_current_admin)
):

    students = load_students()

    if idtodelete not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if students[idtodelete]["roll no"] != rolltodelete:
        raise HTTPException(
            status_code=400,
            detail="CNIC and roll number do not match"
        )

    if confirm_delete != "yes":
        raise HTTPException(
            status_code=400,
            detail="Please confirm deletion"
        )

    del students[idtodelete]

    save_students(students)

    return RedirectResponse(
        url="/admin/dashboard",
        status_code=303
    )


@app.post("/admin/students/update")
def update_student(
    toupdate: str = Form(...),
    rolltoupdate: str = Form(...),
    name: str = Form(""),
    age: str = Form(""),
    city: str = Form(""),
    Department: str = Form(""),
    gpa: str = Form("")
):
    students = load_students()

    # Find student using CNIC
    if toupdate not in students:
        return HTMLResponse(
            "Student with this CNIC was not found.",
            status_code=404
        )

    student = students[toupdate]

    # Verify roll number
    if student.get("roll no") != rolltoupdate:
        return HTMLResponse(
            "Roll number does not match this student.",
            status_code=400
        )

    # Update only fields that are not empty
    if name.strip():
        student["name"] = name.strip()

    if age.strip():
        try:
            student["age"] = int(age)
        except ValueError:
            return HTMLResponse("Invalid age.", status_code=400)

    if city.strip():
        student["city"] = city.strip()

    if Department.strip():
        student["major"] = Department

    if gpa.strip():
        try:
            student["gpa"] = float(gpa)
        except ValueError:
            return HTMLResponse("Invalid GPA.", status_code=400)

    # Save updated student records
    save_students(students)

    return RedirectResponse(
        url="/admin/dashboard",
        status_code=303
    )



def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

