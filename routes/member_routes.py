from fastapi import APIRouter

from database.member_db import MemberDb
from database.db_connection import get_connection, logger

router = APIRouter()
db_conn = get_connection()
my_members_db = MemberDb(db_conn)


@router.post("/members", status_code=200)
def create_new_member(data: dict):
    logger.info("GET /members")
    return my_members_db.create_member(data)

@router.get("/members")
def get_all_members():
    return my_members_db.get_all_members()

@router.get("/members/{id}")
def get_member_by_id(id: int):
    return my_members_db.get_member_by_id(id)