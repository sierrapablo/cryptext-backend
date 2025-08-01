from fastapi import FastAPI
from .routes import notes


app = FastAPI(title="CrypText API")

app.include_router(notes.router, prefix="/notes", tags=["notes"])
