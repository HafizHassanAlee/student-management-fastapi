from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import json
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )

@app.get("/students/{roll}")
def students(request: Request, roll: str):
    with open("students.json", "r") as file:
        x = json.load(file)
    for i in x.values():
        if i["roll no"] == roll:
            data = i
            break
    return templates.TemplateResponse(
                request=request,
                name="students.html",
                context={"student": data},
            )