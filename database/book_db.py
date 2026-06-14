from fastapi import HTTPException

GENRE_VALUES = ('Fiction', 'Non-Fiction', 'Science', 'History', 'Other')


class BookDB:
    def __init__(self, db_connection):
        self.connection = db_connection

    def create_book(self, data):
        if data["genre"] in GENRE_VALUES:
            cursor = self.connection.cursor()
            sql = "INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)"
            val = (data["title"], data["author"], data["genre"])
            cursor.execute(sql, val)
            self.connection.commit()
            return data
        raise HTTPException(status_code=422, detail="The genre entered is not 'Fiction', 'Non-Fiction', 'Science', 'History', 'Other'")


    def get_all_books(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books")
        desc = cursor.fetchall()
        row = []
        for i in desc:
            row.append({"id": i[0], "title": i[1], "author": i[2], "genre": i[3], "is_available": i[4], "borrowed_by_number_id": i[5]})
        cursor.close()
        return row


    def get_book_by_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        desc = cursor.fetchall()
        row = []
        for i in desc:
            if i["id"] == id:
                row.append(i)
        if row == []:
            raise HTTPException(status_code=404, detail="not fo0und")
        cursor.close()
        return row

    def update_book(self, id, data):
        cursor = self.connection.cursor(dictionary=True)
        try:

            set_parts = [f"{key} = %s" for key in data.keys()]
            set_cluse = ", ".join(set_parts)

            sql = f"UPDATE books SET {set_cluse} WHERE id = %s"
            val = list(data.values()) + [id]

            cursor.execute(sql, val)

            changed = cursor.rowcount > 0

            self.connection.commit()
            cursor.close()
            return changed
        except:
            raise HTTPException(status_code=404, detail="not fo0und")


    def set_available(self, id, val, member_id):
        cursor = self.connection.cursor(dictionary=True)
        if val == True:
            query = "UPDATE books SET is_available = 1, borrowed_by_number_id = %s WHERE id = %s AND is_available = 0"
            cursor.execute(query, (member_id, id))
            self.connection.commit()
            changed = cursor.rowcount > 0
            if changed == True:
                return True
            raise HTTPException(status_code=404, detail="not fo0und")
        query = "UPDATE books SET is_available = 0, borrowed_by_number_id = NULL WHERE id = %s AND is_available = 1"
        cursor.execute(query, (id,))
        self.connection.commit()
        changed = cursor.rowcount > 0
        if changed == True:
            return True
        raise HTTPException(status_code=404, detail="not fo0und")

    def count_active_borrows_by_member(self, member_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT COUNT(*) as count FROM books WHERE borrowed_by_number_id = %s"
        cursor.execute(query, (member_id,))
        result = cursor.fetchone()

        return result["count"] < 3


    def count_borrowed_books(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(is_available) as count FROM books WHERE is_available = 0")
        counter = cursor.fetchone()
        return counter["count"]


    def count_available_books(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(is_available) as count FROM books WHERE is_available = 1")
        counter = cursor.fetchone()
        return counter["count"]


    def count_by_genre(self, genre):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT genre, COUNT(*) as count FROM books GROUP BY Genre")
        counter = cursor.fetchall()
        new_list = []
        for book in counter:
            new_list.append(book)
        return new_list






