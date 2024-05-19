from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ContactSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: Optional[str] = Field(max_length=100)
    phone_number: str = Field(max_length=20)
    birthday: Optional[date]
    additional_info: Optional[str] = Field(max_length=255)

    @field_validator("birthday", mode="before")
    def validate_birthday(cls, value):
        if value:
            if isinstance(value, str):
                try:
                    parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Birthday must be in format YYYY-MM-DD")
            else:
                parsed_date = value
            return parsed_date
        return value


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponse(ContactSchema):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_info: str

    class Config:
        orm_mode = True
