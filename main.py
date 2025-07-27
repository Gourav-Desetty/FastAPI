from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

conn = MongoClient("mongodb+srv://Gourav:Gourav@cluster0.p5ihobp.mongodb.net")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    newdocs=[]
    docs = conn.notes.notes.find({})
    for doc in docs:
        newdocs.append({
            "id" : doc["_id"],
            "note" : doc["note"]
        })
    return templates.TemplateResponse(
        "index.html",  # template filename first
        {"request": request, "newdocs": newdocs}
    )


