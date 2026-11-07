# from flask import Flask

# # Create our Flask application
# app = Flask(__name__)

# # Create a website route
# @app.route("/")
# def home():
#     return "Welcome to Class Pearl!"

# # Start the development server
# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)


@app.route("/")
@app.route("/dashboard")
def dashboard():
    search_query = request.args.get("search", "").strip()

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if search_query:
            cursor.execute(
                """
                SELECT * FROM students
                WHERE name LIKE %s
                ORDER BY id ASC
                """,
                (f"%{search_query}%",)
            )
        else:
            cursor.execute(
                "SELECT * FROM students ORDER BY id ASC"
            )

        students = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS total FROM students")
        total_students = cursor.fetchone()["total"]

        cursor.execute(
            """
            SELECT COUNT(DISTINCT subject) AS total
            FROM students
            WHERE subject IS NOT NULL
            """
        )
        total_subjects = cursor.fetchone()["total"]

        total_results = len(students)

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "dashboard.html",
        students=students,
        total_students=total_students,
        total_subjects=total_subjects,
        total_results=total_results,
        search_query=search_query
    )


@app.route("/add", methods=["GET"])
def add_page():
    return render_template("add_student.html")


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    age_text = request.form.get("age", "").strip()
    subject = request.form.get("subject", "").strip()

    if not name or not age_text or not subject:
        return "All fields are required.", 400

    try:
        age = int(age_text)
    except ValueError:
        return "Age must be a number.", 400

    if not 1 <= age <= 120:
        return "Enter a valid age.", 400

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (name, age, subject)
            VALUES (%s, %s, %s)
            """,
            (name, age, subject)
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
