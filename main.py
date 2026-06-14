import uvicorn

from database import db_connection
from fastapi import FastAPI
from routes.book_routes import router as book_routes
from routes.member_routes import router as member_routes
from routes.report_routes import router as report_routes

app = FastAPI()

app.include_router(book_routes)
app.include_router(member_routes)
app.include_router(report_routes)


def main():
    db_connection.create_tables()

if __name__ == "__main__":
    main()
    uvicorn.run("main:app", port=8003)