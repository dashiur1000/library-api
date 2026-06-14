from fastapi import APIRouter
from database.member_db import MemberDb
from database.book_db import BookDB
from database.db_connection import get_connection, logger


router = APIRouter()
db_conn = get_connection()
my_reports_member = MemberDb(db_conn)
my_reports_books = BookDB(db_conn)

@router.get("/reports/summary")
def reports_all():
    return {"total_books": my_reports_books.count_borrowed_books()+my_reports_books.count_available_books(),
            "available_books": my_reports_books.count_available_books(),
            "currently_borrowed": my_reports_books.count_borrowed_books(),
            "active_members": my_reports_member.count_active_members()}

@router.get("/reports/books-by-genre")
def count_by_genre(genre):
    pass