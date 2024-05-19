from sqlalchemy import Date, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    birthday: Mapped[Date] = mapped_column(Date)
    additional_info: Mapped[str] = mapped_column(String(255))
