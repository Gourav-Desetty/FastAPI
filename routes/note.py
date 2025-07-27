from fastapi import APIRouter
from models.note import Note
from config.db import conn
from schemas.note import noteEntity, notesEntity
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

note=APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    newdocs=[]
    docs = conn.notes.notes.find({})
    for doc in docs:
        newdocs.append({
            "id" : doc["_id"],
            "title" : doc["title"],
            "desc" : doc["desc"],
            "important":doc["important"]
        })
    return templates.TemplateResponse(
        "index.html",  # template filename first
        {"request": request, "newdocs": newdocs}
    )   

@note.post("/", response_class=HTMLResponse)
async def create_item(request: Request):
    form = await request.form()
    note = conn.notes.notes.insert_one(dict(form))
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "newdocs": conn.notes.notes.find({})}
    )