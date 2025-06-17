from app.routers.notes import router as notes_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(notes_router)
