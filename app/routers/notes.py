from app.core.db import engine
from app.models.note import NoteOrm
from app.schemas.note import (
    NoteReadSchema, NoteIdSchema, NoteCreateSchema, NoteCountSchema
)
from app.dependencies import AdminDep

from app.helpers.auto_deletion import autodelete_job
from app.helpers.crypto import decrypt_and_decompress, encrypt_and_compress

from fastapi import status
from fastapi.routing import APIRouter
from fastapi import BackgroundTasks, HTTPException

from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix='/notes')


@router.get("/count", response_model=int)
async def get_count():
    count = await engine.count(NoteOrm)
    return count


@router.get("/{note_id}", response_model=NoteReadSchema)
async def get_note(note_id: str, password: str, background_tasks: BackgroundTasks):
    try:
        note = await engine.find_one(NoteOrm, {"_id": ObjectId(note_id)})
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"note {note_id} not found")
        
        content = decrypt_and_decompress(note.content, password)

        background_tasks.add_task(autodelete_job, note_id)

        return {"content": content}
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad id")


@router.post("/create", response_model=NoteIdSchema)
async def create_note(note_input: NoteCreateSchema):
    encrypted_content = encrypt_and_compress(note_input.content, note_input.password)
    new_note = NoteOrm(content=encrypted_content)
    return await engine.save(new_note)


@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
async def delete_note(note_id: str, is_admin: AdminDep, password: str | None = None):
    try:
        note = await engine.find_one(NoteOrm, {"_id": ObjectId(note_id)})
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"note {note_id} not found")
        
        if password:
            decrypt_and_decompress(note.content, password)
            await engine.delete(note)
            return

        if not is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access denied")
        
        await engine.delete(note)

    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad id")
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access denied")
