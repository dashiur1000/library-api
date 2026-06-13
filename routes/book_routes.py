from fastapi import FastAPI, HTTPException
import uvicorn
from database.book_db import BookDB
from database.db_connection import get_connection

app = FastAPI()
db_conn = get_connection()
my_book_db = BookDB(db_conn)


@app.post("/books")
def create_book(data: dict):
    return {"create_book": my_book_db.create_book(data)}

@app.get("/books")
def get_books():
    return my_book_db.get_all_books()

@app.get("/books/{id}")
def get_by_id(id: int):
    return my_book_db.get_book_by_id(id)

@app.put("/books/{id}")
def update_book(id: int, data: dict):
    return my_book_db.update_book(id, data)

@app.put("/books/{id}/borrow/{member_id}")
def borrow_book(id, member_id):
    return my_book_db.set_available(id, my_book_db.count_active_borrows_by_member(member_id), member_id)

@app.put("/books/{id}/return/{member_id}")
def return_book(id, member_id):
    return my_book_db.set_available(id, False, member_id)





if __name__ == "__main__":
    uvicorn.run("book_routes:app", port=8001)