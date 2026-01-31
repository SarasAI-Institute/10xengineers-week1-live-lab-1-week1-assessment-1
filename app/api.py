from fastapi import FastAPI, HTTPException
from typing import List, Optional
from app.models import Book, BookCreate, Member, MemberCreate, Loan, LoanCreate
from app.storage import books, members, loans
from app.utils import gen_id, now, calc_due, check_overdue, get_fine

app = FastAPI()

@app.get("/books")
def list_books(genre: Optional[str] = None):
    b = list(books.values())
    if genre:
        b = [x for x in b if x.genre == genre]
    return b

@app.get("/books/{book_id}")
def get_book(book_id: str):
    if book_id not in books:
        raise HTTPException(404)
    return books[book_id]

@app.post("/books")
def add_book(data: BookCreate):
    b = Book(
        id=gen_id(),
        title=data.title,
        author=data.author,
        isbn=data.isbn,
        copies=data.copies,
        available=data.copies,
        genre=data.genre
    )
    books[b.id] = b
    return b

@app.get("/members")
def list_members():
    return list(members.values())

@app.post("/members")
def add_member(data: MemberCreate):
    m = Member(
        id=gen_id(),
        name=data.name,
        email=data.email,
        joined=now()
    )
    members[m.id] = m
    return m

@app.get("/loans")
def list_loans(overdue_only: bool = False):
    l = list(loans.values())
    if overdue_only:
        l = [x for x in l if check_overdue(x)]
    return l

@app.post("/loans")
def create_loan(data: LoanCreate):
    if data.book_id not in books:
        raise HTTPException(404, "book not found")
    if data.member_id not in members:
        raise HTTPException(404, "member not found")
    book = books[data.book_id]
    if book.available < 1:
        raise HTTPException(400, "no copies available")
    book.available -= 1
    loan = Loan(
        id=gen_id(),
        book_id=data.book_id,
        member_id=data.member_id,
        borrowed=now(),
        due=calc_due()
    )
    loans[loan.id] = loan
    return loan

@app.post("/loans/{loan_id}/return")
def return_book(loan_id: str):
    if loan_id not in loans:
        raise HTTPException(404)
    loan = loans[loan_id]
    if loan.returned:
        raise HTTPException(400, "already returned")
    loan.returned = now()
    books[loan.book_id].available += 1
    fine = get_fine(loan)
    return {"loan": loan, "fine": fine}

@app.get("/members/{member_id}/loans")
def member_loans(member_id: str):
    if member_id not in members:
        raise HTTPException(404)
    return [l for l in loans.values() if l.member_id == member_id]

