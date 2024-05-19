from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as repository_contacts

from ..schemas import ContactResponse, ContactSchema, ContactUpdateSchema

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(
    limit: int = Query(default=10, ge=10, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found",
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}")
async def update_contact(
    body: ContactUpdateSchema, contact_id: int, db: AsyncSession = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found",
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found",
        )
    return contact


@router.get("/search/", response_model=list[ContactResponse])
async def search_contacts(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    contacts = await repository_contacts.search_contacts(
        first_name, last_name, email, db
    )
    return contacts


@router.get("/birthdays/", response_model=list[ContactResponse])
async def get_birthdays(db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.get_birthdays(db)
    return contacts
