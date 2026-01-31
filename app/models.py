from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Book(BaseModel):
    id: str
    title: str
    author: str
    isbn: str
    copies: int
    available: int
    genre: Optional[str] = None

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    copies: int = 1
    genre: Optional[str] = None

class Member(BaseModel):
    id: str
    name: str
    email: str
    joined: datetime
    active: bool = True

class MemberCreate(BaseModel):
    name: str
    email: str

class Loan(BaseModel):
    id: str
    book_id: str
    member_id: str
    borrowed: datetime
    due: datetime
    returned: Optional[datetime] = None

class LoanCreate(BaseModel):
    book_id: str
    member_id: str

