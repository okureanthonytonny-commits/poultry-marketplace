from fastapi import APIRouter, Depends
from sqlmodel import select
from app.core.database import get_session
from app.models import Item
from app.schemas import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=list[ItemRead])
def list_items(session=Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items

@router.post("", response_model=ItemRead, status_code=201)
def create_item(item: ItemCreate, session=Depends(get_session)):
    db_item = Item(name=item.name)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
