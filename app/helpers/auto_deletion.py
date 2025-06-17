from app.core.db import engine
from app.models.note import NoteOrm

from bson import ObjectId


async def autodelete_job(note_id: str):
    note = await engine.find_one(NoteOrm, {"_id": ObjectId(note_id)})
    await engine.delete(note)
