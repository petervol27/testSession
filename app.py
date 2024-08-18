from flask import Flask, url_for, redirect, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "sha250db12"


def get_connection():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS cars(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,number UNIQUE,description,img,urgent DEFAULT 0)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, email,password,username)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS problems(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,name,price,represent)"
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS carProblems(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,carId INTEGER ,problemId INTEGER,FOREIGN KEY(carId) REFERENCES cars(id)  ON DELETE CASCADE,
        FOREIGN KEY(problemId) REFERENCES problems(id))"""
    )
    conn.commit()
    conn.close()


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
        cursor.execute(
            f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}' "
        )
        row = cursor.fetchone()
        if row:
            user = dict(row)
            print(user)
            session["logged_in"] = True
            session["username"] = user.get("username")

            return redirect(url_for("car_list"))
    return render_template("login.html")


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/car_list/")
def car_list():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch cars and their associated problems
    query = """
    SELECT 
        cars.id AS car_id,
        cars.number,
        cars.description,
        cars.img,
        cars.urgent,
        problems.represent AS problem_represent
    FROM 
        cars
    LEFT JOIN 
        carProblems ON cars.id = carProblems.carId
    LEFT JOIN 
        problems ON carProblems.problemId = problems.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cars = {}
    for row in rows:
        car_id = row["car_id"]
        if car_id not in cars:
            cars[car_id] = {
                "id": car_id,
                "number": row["number"],
                "description": row["description"],
                "img": row["img"],
                "urgent": row["urgent"],
                "problems": [],
            }
        if row["problem_represent"]:
            cars[car_id]["problems"].append(row["problem_represent"])

    car_list = list(cars.values())

    return render_template("car_list.html", cars=car_list)


@app.route("/add_car/", methods=["GET", "POST"])
def add_car():
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        urgent = 1 if request.form.get("urgent") == "on" else 0
        new_car = [
            request.form["number"],
            request.form["description"],
            request.form["img"],
            urgent,
        ]
        cursor.execute(
            """INSERT INTO Cars (number, description, img, urgent) VALUES (?, ?, ?, ?)""",
            new_car,
        )
        car_id = cursor.lastrowid
        selected_problems = request.form.getlist("problems")
        for problem_id in selected_problems:
            cursor.execute(
                "INSERT INTO CarProblems (carId, problemId) VALUES (?, ?)",
                (car_id, problem_id),
            )
        conn.commit()
        conn.close()
        return redirect(url_for("car_list"))
    cursor.execute("SELECT * FROM Problems")
    problems = cursor.fetchall()
    conn.close()
    return render_template("add_car.html", problems=problems)


@app.route("/delete/<id>/")
def delete_car(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CarProblems WHERE carId=?", (id,))
    cursor.execute("DELETE FROM cars WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("car_list"))


@app.route("/edit_car/<id>/", methods=["POST", "GET"])
def edit_car(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE id=?", (id,))
    row = cursor.fetchone()
    car = dict(row)
    cursor.execute("SELECT * FROM problems")
    all_problems = cursor.fetchall()
    cursor.execute("SELECT problemId FROM carProblems WHERE carId=?", (id,))
    current_problems = [row["problemId"] for row in cursor.fetchall()]
    if request.method == "POST":
        urgent = 1 if request.form.get("urgent") == "on" else 0
        cursor.execute(
            """UPDATE cars SET number=?, description=?, img=?, urgent=? WHERE id=?""",
            [
                request.form["number"],
                request.form["description"],
                request.form["img"],
                urgent,
                id,
            ],
        )
        selected_problems = request.form.getlist("problems")
        cursor.execute("DELETE FROM carProblems WHERE carId=?", (id,))
        for problem_id in selected_problems:
            cursor.execute(
                "INSERT INTO carProblems (carId, problemId) VALUES (?, ?)",
                (id, problem_id),
            )
        conn.commit()
        conn.close()
        return redirect(url_for("car_list"))
    conn.close()
    return render_template(
        "edit_car.html",
        car=car,
        all_problems=all_problems,
        current_problems=current_problems,
    )


# @app.route("/forms/")
# def forms():
#     conn = get_connection()
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#     cursor = cursor.execute(f"SELECT * FROM cars WHERE id=1")
#     row = cursor.fetchone()
#     car = dict(row)
#     return render_template("forms.html", action="edit_car", car=car)


if __name__ == "__main__":
    create_tables()
    app.run(debug=True, port=9000)
