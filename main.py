from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
import json
from fastapi.staticfiles import StaticFiles
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.responses import RedirectResponse 
from fastapi import Form
from fastapi.responses import JSONResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


SECRET_KEY = "d05b3e1db534c9cdcf5b0190faaadfbc48f474034fb4a49498982e5d5a849477"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.get("/")
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

