from datetime import date, timedelta
from typing import Optional

from sqlalchemy import and_, extract, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact

from ..schemas import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()

    if contact is None:
        return None

    await db.delete(contact)
    await db.commit()
    return contact


async def search_contacts(
    first_name: Optional[str],
    last_name: Optional[str],
    email: Optional[str],
    db: AsyncSession,
):
    query = select(Contact)

    filters = []
    if first_name:
        filters.append(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        filters.append(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        filters.append(Contact.email.ilike(f"%{email}%"))

    if filters:
        query = query.filter(or_(*filters))

    result = await db.execute(query)
    return result.scalars().all()


async def get_birthdays(db: AsyncSession):
    today = date.today()
    upcoming_date = today + timedelta(days=7)

    query = select(Contact).filter(
        or_(
            and_(
                extract("month", Contact.birthday) == today.month,
                extract("day", Contact.birthday) >= today.day,
            ),
            and_(
                extract("month", Contact.birthday) == upcoming_date.month,
                extract("day", Contact.birthday) <= upcoming_date.day,
            ),
        )
    )

    result = await db.execute(query)
    return result.scalars().all()
