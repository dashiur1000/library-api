from fastapi import FastAPI, HTTPException
import uvicorn

from database.member_db import MemberDb
from database.db_connection import get_connection

app = FastAPI()
db_conn = get_connection()
my_members_db = MemberDb(db_conn)


@app.post("/members", status_code=200)
def create_new_member(data: dict):
    return my_members_db.create_member(data)

@app.get("/members")
def get_all_members():
    return my_members_db.get_all_members()

if __name__ == "__main__":
    uvicorn.run("member_routes:app", port=8002)