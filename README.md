# Welcome to the library system!

## System description
A library management system with all that this implies, book management and subscription management and the integration between them.

In the database, there are two databases: books and members.

In the system, you can add and manage books, add and manage members



## The code to create docker with MySql
### step 1
````
docker run --name my-mysql1 \
-e MYSQL_ROOT_PASSWORD=secret \
-e MYSQL_DATABASE=mydb \
-p 3308:3306 \
-d mysql:latest
````
### step 2
````
docker ps
````
### step 3
````
docker exec -it my-mysql1 mysql -u root -p
````
### step 4
````
password: secret
````
### step 5
````
SHOW DATABASES;
USE mydb;
SHOW TABLES;
````

## Folder structure

````
library-api/
│
│
├── main.py
├── database/
│ ├── db_connection.py
│ ├── book_db.py
│ └── member_db.py
├── routes/
│ ├── book_routes.py
│ ├── member_routes.py
│ └── report_routes.py
├── logs/
│ └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore
````

## Table structure
### books table
| field | explanation                                                                                                                                                                     |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id    | primary key - int - automatic numbering                                                                                                                                         |
| title | Book title, non-empty column, maximum 50 characters - str                                                                                                                       |
| author| Author name, non-empty column, maximum 50 characters - str                                                                                                                      |
| genre | Allowed genre values: Implemented — Fiction Non-Fiction \ Science \ History \ Other as an ENUM column in the database, any other value returns an error, Non-empty column - str |
| available_is | Is the book available for loan — FALSE indicates loaned Non-empty column - bool                                                                                                 |
| id_member_by_borrowed | The ID of the member holding the book — NULL if available - int or null                                                                                                         |

### members table
| field     | explanation                                                                             |
|-----------|-----------------------------------------------------------------------------------------|
| id        | primary key - int - automatic numbering                                                 |
| name      | Member name, non-empty column, maximum 50 characters - str                              |
| email     | Email address — unique, non-empty column - str                                          |
| is_active | Is the member active — FALSE Cannot borrow a non-empty column - bool                    |
| total_borrows | Total number of questions - increases by 1 - each question has a non-empty column - int |


## System rules
| law |subject| rule                                                                                                                                  |
|-----|-------|---------------------------------------------------------------------------------------------------------------------------------------|
| 1   |Creating a book| User sends genre/author/title — system adds is_available=True, borrowed_by=NULL                                                       |
| 2   |genre| Must be Fiction / Non-Fiction / Science / History / Othe - Any other value returns an error. Make sure to check both the POST and PUT |
| 3   |Create a friend| The user sends name/email The system adds is_active = True, total_borrows = 0                                                         |
| 4   |email| Must be unique — if it already exists returns an error                                                                                |
| 5   |Inactive member| if is_active = False - You can't borrow a book                                                                                        | 
| 6   |Book not available|You cannot borrow a book that is already borrowed (is_available = False)|
| 7   |Maximum Books | A member cannot hold more than 3 books at a time|
| 8   |Returning a book|A book can only be returned if it is lent to the same friend who is returning it|


## Endpoints list
### Books
| Method | Endpoint | Description                                                                                                   | Request Body               | Response                                                                                         |func|
|-----|--------|---------------------------------------------------------------------------------------------------------------|----------------------------|--------------------------------------------------------------------------------------------------|-|
|POST|/books| create a book                                                                                                 | INSERT to books table      | {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "genre": "Fiction"} |create_book(data)|
|GET|/books| get all books                                                                                                 | SELECT all books           |                                                                                                  |get_all_books()|
|GET|/books/{id}| get book by id or None                                                                                        | SELECT books by id         | id                                                                                               |get_book_by_id(id)|
|PUT|/books/{id}| update book                                                                                                   | UPDATE book by id and data | {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "genre": "Fiction"} |update_book(id, data)|
|PUT|/books/{id}/borrow/{number_id}| Lending a book to a friend by id and number id from the friend, update is_available and borrowed_by_member_id | UPDATE book by id and id number| id, val, number_id                                                                               |set_available(id, val, member_id), count_active_borrows_by_member(member_id)|
|PUT|/books/{id}/return/{number_id}| Returning a book from an author,  update is_available and borrowed_by_member_id| UPDATE book by id and id number| id, val, number_id                                                                               |set_available(id, val, member_id)|

### Members
| Method | Endpoint | Description                                                                                                   | Request Body                 | Response                                            |func|
|------|--------|---------------------------------------------------------------------------------------------------------------|------------------------------|-----------------------------------------------------|-|
|POST|/members|create friend| INSERT to members table      | {"name": "Sara Cohen", "email": "sara@example.com"} |create_member(data)|
|GET|/members|get all friends| SELECT all members           |                                                     |get_all_members()|
|GET|/members{id}| get all friends by id| SELECT all members by id     | id                                                  |get_member_by_id(id|
|PUT|/members{id}|update member| UPDATE member by id and data | {"name": "Sara Cohen", "email": "sara@example.com"} |update_member(id, data)|
|PUT|/members{id}/deactivate|Disabling a friend| UPDATE is_active=False       | id                                                  |deactivate_member(id)|
|PUT|/members{id}/activate| Member activation| UPDATE is_active=True | id| activate_member(id)|

### Reports
| Method | Endpoint | Description        | Request Body  | Response | func                     |
|------|--------|--------------------|------------|-----------------------|--------------------------|
|GET|/reports/summary | get general report |SELECT members is_active=True|| count_active_members(),  count_available_books()|
|GET|/reports/books-by-genre|Book Writer by Genre|SELECT books GROUP BY Genre|| count_by_genre(genre)    |
|GET|/reports/top-member| Returns the most active member| SELECT by borrows_total|| get_top_member()         |


## System flow
1. **Server Startup:**
   - The server connects to MySQL
   - Creates tables if they don't exist
   - Starts the FastAPI server

2. **Creating a Member:**
   - User sends POST request to `/members` with name and email
   - System validates the email is unique
   - System creates member with `is_active=True` and `total_borrows=0`
   - Returns the created member

3. **Borrowing a Book:**
   - User sends PUT request to `/books/{id}/borrow/{member_id}`
   - System checks if book exists
   - System checks if member exists and is active
   - System checks if book is available
   - System checks if member has less than 3 books
   - Updates book: `is_available=False`, `borrowed_by_member_id=member_id`
   - Increments member's `total_borrows` by 1
   - Returns success message

4. **Updating a friend's details:**
   - User sends a PUT request to `/members{id}`
   - User enters all updated details as a dictionary
   - System updates the details in the database
   - Returns success message

5. **Updating a friend's active:**
   - User sends a PUT request to `/members/{id}`
   - User sends a PUT request to `/members{id}/deactivate`
   - If the member is true and wants to change it to false
   - User sends a PUT request to `/members/{id}/deactivate`
   - If the member is false and wants to change it to true
   - User sends a PUT request to `/members/{id}/activate`
   - Returns success message

6. **View all books:**
   - User sends a GET request to `/books`

7. **View book by id:**
   - User sends a GET request to `/books/{id}`

8. **update a book:**
   - User sends a GET request to `/books/{id}`
   - User sends a PUT request to `/books/{id}`
   - Returns success message

9. **Borrowing a book from a member:**
   - User sends a GET request to `/books/{id}`
   - If the book has not been borrowed and exists
   - User sends a request to `/books/{id}/borrow/{member_id}`
   - User checks if it is allowed to borrow
   - If so, update the book and update the member
   - Notification that the book has been borrowed

10. **Additional actions:**
   - Show all members GET `/members`
   - Show general report GET `/reports/summary`
   - Show all books by genre GET `/reports/books-by-genre`
   - Show most active member GET `/reports/top-member`


## Running instructions
### step 1
Download the Python files via the clone on GitHub
````
https://github.com/dashiur1000/library-api.git
````
### step 2
Install the requirements.txt file to install all the libraries
````
pip install requirements.txt
````
### step 3
Install Docker as per the instructions given above at the beginning of the file
### step 4
Open the main.py and start the server or by running
### step 5
Open the swagger to view and manage the server