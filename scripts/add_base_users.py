import sqlite3

users = [
    {
        "id": 1,
        "email": "admin@admin.com",
        "password": "admin123",
        "username": "Admin-Man",
    },
    {"id": 2, "email": "user@user.com", "password": "user123", "username": "User-Man"},
]


con = sqlite3.connect("data.db")
cur = con.cursor()
for user in users:
    cur.execute(
        """INSERT INTO users(id,email,password,username) VALUES(?,?,?,?)
          """,
        (
            user["id"],
            user["email"],
            user["password"],
            user["username"],
        ),
    )
con.commit()
con.close()
