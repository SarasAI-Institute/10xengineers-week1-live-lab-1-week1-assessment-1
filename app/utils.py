import uuid
from datetime import datetime, timedelta

def gen_id():
    return str(uuid.uuid4())[:8]

def now():
    return datetime.now()

def calc_due(days=14):
    return datetime.now() + timedelta(days=days)

def check_overdue(loan):
    if loan.returned:
        return False
    return datetime.now() > loan.due

def get_fine(loan, rate=0.5):
    if not check_overdue(loan):
        return 0
    days = (datetime.now() - loan.due).days
    return days * rate

def format_book_info(book, include_availability=True, verbose=False, show_genre=True, indent=0):
    s = ""
    ind = " " * indent
    if verbose:
        s = s + ind + "=" * 30 + "\n"
    s = s + ind + "Title: " + book.title + "\n"
    s = s + ind + "Author: " + book.author + "\n"
    s = s + ind + "ISBN: " + book.isbn + "\n"
    if show_genre and book.genre:
        s = s + ind + "Genre: " + book.genre + "\n"
    if include_availability:
        s = s + ind + "Available: " + str(book.available) + "/" + str(book.copies) + "\n"
    if verbose:
        s = s + ind + "=" * 30 + "\n"
    return s

def search_books(books_list, q, field="title"):
    r = []
    for b in books_list:
        if field == "title":
            if q.lower() in b.title.lower():
                r.append(b)
        elif field == "author":
            if q.lower() in b.author.lower():
                r.append(b)
        elif field == "isbn":
            if q in b.isbn:
                r.append(b)
    return r

def get_member_loans(loans_list, member_id):
    return [l for l in loans_list if l.member_id == member_id and not l.returned]

