from fastapi import FastAPI, HTTPException

class MemberDb:
    def __init__(self, db_connection):
        self.connection = db_connection

    def create_member(self, data: dict):
        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO members (name, email, is_active, total_borrows) VALUES (%s, %s, %s, %s)"
            val = (data["name"], data["email"], True, 0)
            cursor.execute(sql, val)
            self.connection.commit()
            return data
        except:
            raise HTTPException(status_code=422, detail="Non-standard dictionary")


    def get_all_members(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM members")
        val = cursor.fetchall()
        my_list = []
        for i in val:
            my_list.append({"member_id": i[0], "name": i[1], "email": i[2], "is_active": i[3], "total_borrows": i[4]})
        return my_list


    def get_member_by_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members")
        val = cursor.fetchall()
        row = []
        for item in val:
            if item["id"] == id:
                row.append(item)
        if row == []:
            raise HTTPException(status_code=404, detail="Member does not exist")
        return row


    def update_member(self, id, data):
        cursor = self.connection.cursor(dictionary=True)
        try:
            set_parts = [f"{key} = %s" for key in data.keys()]
            set_cluse = ", ".join(set_parts)

            sql = f"UPDATE members SET {set_cluse} WHERE id = %s"
            val = (list(data.values())) + [id]

            cursor.execute(sql, val)
            changed = cursor.rowcount > 0
            self.connection.commit()
            cursor.close()

            return changed
        except:
            raise HTTPException(status_code=404, detail="not fo0und")



    def deactivate_member(self, id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "UPDATE members SET is_active = 0 WHERE id = %s AND is_active = 1"
            cursor.execute(query, (id,))
            self.connection.commit()
            cursor.close()
            return True
        except:
            raise HTTPException(status_code=404, detail="not found")
