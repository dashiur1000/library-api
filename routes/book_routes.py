from fastapi import APIRouter
from database.book_db import BookDB
from database.db_connection import get_connection, logger

router = APIRouter()
db_conn = get_connection()
my_book_db = BookDB(db_conn)


@router.post("/books")
def create_book(data: dict):
    return {"create_book": my_book_db.create_book(data)}

@router.get("/books")
def get_books():
    logger.info("GET /books")
    return my_book_db.get_all_books()

@router.get("/books/{id}")
def get_by_id(id: int):
    return my_book_db.get_book_by_id(id)

@router.put("/books/{id}")
def update_book(id: int, data: dict):
    return my_book_db.update_book(id, data)

@router.put("/books/{id}/borrow/{member_id}")
def borrow_book(id, member_id):
    return my_book_db.set_available(id, my_book_db.count_active_borrows_by_member(member_id), member_id)

@router.put("/books/{id}/return/{member_id}")
def return_book(id, member_id):
    return my_book_db.set_available(id, False, member_id)