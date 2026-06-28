from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.chat_messages import ChatMessage
from app.utils.auth import get_current_user
from app.schemas.chat_message import ChatMessageCreate, ChatMessageUpdate, ChatMessageResponse
from typing import Optional

chat_message_router = APIRouter()

@chat_message_router.get("/chat_messages")
def list_chat_messages(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    game_id: Optional[int] = Query(None),
    content: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(ChatMessage)
    if game_id is not None:
        query = query.filter(ChatMessage.game_id == game_id)
    if content:
        query = query.filter(ChatMessage.content.ilike(f"%{content}%"))
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return {
        "items": [ChatMessageResponse.from_orm(item) for item in items],
        "total": total,
    }

@chat_message_router.get("/chat_messages/{id}")
def get_chat_message(
    id: int = Path(...),
    db: Session = Depends(get_db),
):
    msg = db.query(ChatMessage).filter(ChatMessage.id == id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Not found")
    return ChatMessageResponse.from_orm(msg)

@chat_message_router.post("/chat_messages", status_code=status.HTTP_201_CREATED)
def create_chat_message(
    msg_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    new_msg = ChatMessage(
        game_id=msg_in.game_id,
        content=msg_in.content,
        user_id=getattr(current_user, "id", None),
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return ChatMessageResponse.from_orm(new_msg)

@chat_message_router.put("/chat_messages/{id}")
def update_chat_message(
    msg_in: ChatMessageUpdate,
    id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    msg = db.query(ChatMessage).filter(ChatMessage.id == id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Not found")
    if msg_in.content is not None:
        msg.content = msg_in.content
    db.commit()
    db.refresh(msg)
    return ChatMessageResponse.from_orm(msg)

@chat_message_router.delete("/chat_messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_message(
    id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    msg = db.query(ChatMessage).filter(ChatMessage.id == id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(msg)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
