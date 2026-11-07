
# from flask import Flask, render_template, request, redirect, url_for
# from db import get_connection

# # Create Flask application
# app = Flask(__name__)


# # ==================================
# # DISPLAY ALL STUDENTS
# # ==================================
# @app.route("/")
# def home():

#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("SELECT * FROM students")
#         students = cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()

#     return render_template("students.html", students=students)


# # ==================================
# # DISPLAY ADD STUDENT FORM
# # ==================================
# @app.route("/add", methods=["GET"])
# def add_page():
#     return render_template("add_student.html")


# # ==================================
# # SAVE NEW STUDENT
# # ==================================
# @app.route("/add", methods=["POST"])
# def add_student():

#     name = request.form.get("name", "").strip()
#     age_text = request.form.get("age", "").strip()
#     subject = request.form.get("subject", "").strip()

#     if not name or not age_text or not subject:
#         return "All fields are required.", 400

#     try:
#         age = int(age_text)
#     except ValueError:
#         return "Age must be a number.", 400

#     if not 1 <= age <= 120:
#         return "Enter a valid age.", 400

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute(
#             """
#             INSERT INTO students (name, age, subject)
#             VALUES (%s, %s, %s)
#             """,
#             (name, age, subject)
#         )

#         connection.commit()

#     finally:
#         cursor.close()
#         connection.close()

#     return redirect(url_for("home"))


# # ==================================
# # DISPLAY EDIT STUDENT FORM
# # ==================================
# @app.route("/edit/<int:id>", methods=["GET"])
# def edit_page(id):

#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute(
#             "SELECT * FROM students WHERE id = %s",
#             (id,)
#         )

#         student = cursor.fetchone()

#     finally:
#         cursor.close()
#         connection.close()

#     if student is None:
#         return "Student not found.", 404

#     return render_template("edit_student.html", student=student)


# # ==================================
# # UPDATE EXISTING STUDENT
# # ==================================
# @app.route("/update/<int:id>", methods=["POST"])
# def update_student(id):

#     name = request.form.get("name", "").strip()
#     age_text = request.form.get("age", "").strip()
#     subject = request.form.get("subject", "").strip()

#     if not name or not age_text or not subject:
#         return "All fields are required.", 400

#     try:
#         age = int(age_text)
#     except ValueError:
#         return "Age must be a number.", 400

#     if not 1 <= age <= 120:
#         return "Invalid age.", 400

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute(
#             """
#             UPDATE students
#             SET name = %s, age = %s, subject = %s
#             WHERE id = %s
#             """,
#             (name, age, subject, id)
#         )

#         connection.commit()

#     finally:
#         cursor.close()
#         connection.close()

#     return redirect(url_for("home"))


# # ==================================
# # DELETE STUDENT
# # ==================================
# @app.route("/delete/<int:id>", methods=["POST"])
# def delete_student(id):

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute(
#             "DELETE FROM students WHERE id = %s",
#             (id,)
#         )

#         connection.commit()

#     finally:
#         cursor.close()
#         connection.close()

#     return redirect(url_for("home"))


# # ==================================
# # RUN FLASK APPLICATION
# # ==================================
# if __name__ == "__main__":
#     app.run(debug=True)




from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
from db import get_connection

app = Flask(__name__)

# Required for Flask flash messages
app.secret_key = "student_management_secret_key"


# -----------------------------------
# FORM VALIDATION FUNCTION
# -----------------------------------

def validate_student_form():

    name = request.form.get("name", "").strip()
    age_text = request.form.get("age", "").strip()
    subject = request.form.get("subject", "").strip()

    if not name or not age_text or not subject:
        return None, "All fields are required."

    if len(name) < 2:
        return None, "Student name must contain at least 2 characters."

    if not name.replace(" ", "").isalpha():
        return None, "Name must contain letters only."

    try:
        age = int(age_text)
    except ValueError:
        return None, "Age must be a valid number."

    if age < 1 or age > 120:
        return None, "Age must be between 1 and 120."

    if len(subject) < 2:
        return None, "Subject must contain at least 2 characters."

    return {
        "name": name,
        "age": age,
        "subject": subject
    }, None
# -----------------------------------
# HOME: VIEW, SEARCH, FILTER, STATISTICS
# -----------------------------------

@app.route("/")
def home():

    search = request.args.get("search", "").strip()
    subject_filter = request.args.get("subject", "").strip()

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        # Build the search query
        sql = "SELECT * FROM students WHERE 1=1"
        values = []

        # Search students by name
        if search:
            sql += " AND name LIKE %s"
            values.append("%" + search + "%")

        # Filter students by subject
        if subject_filter:
            sql += " AND subject = %s"
            values.append(subject_filter)

        sql += " ORDER BY id DESC"

        cursor.execute(sql, values)
        students = cursor.fetchall()

        # Get total number of students
        cursor.execute("SELECT COUNT(*) AS total FROM students")
        total_students = cursor.fetchone()["total"]

        # Get number of different subjects
        cursor.execute(
            "SELECT COUNT(DISTINCT subject) AS total FROM students"
        )
        total_subjects = cursor.fetchone()["total"]

        # Get average student age
        cursor.execute(
            "SELECT AVG(age) AS average_age FROM students"
        )
        average_age = cursor.fetchone()["average_age"]

        # Get subjects for the filter dropdown
        cursor.execute(
            "SELECT DISTINCT subject FROM students ORDER BY subject"
        )
        subjects = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "students.html",
        students=students,
        search=search,
        subject_filter=subject_filter,
        subjects=subjects,
        total_students=total_students,
        total_subjects=total_subjects,
        average_age=round(average_age, 1) if average_age is not None else 0
    )


# -----------------------------------
# ADD STUDENT: DISPLAY FORM
# -----------------------------------

@app.route("/add", methods=["GET"])
def add_page():
    return render_template("add_student.html")


# -----------------------------------
# ADD STUDENT: SAVE TO MYSQL
# -----------------------------------

@app.route("/add", methods=["POST"])
def add_student():

    student, error = validate_student_form()

    if error:
        flash(error, "error")
        return redirect(url_for("add_page"))

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (name, age, subject)
            VALUES (%s, %s, %s)
            """,
            (
                student["name"],
                student["age"],
                student["subject"]
            )
        )

        connection.commit()
    finally:
        cursor.close()
        connection.close()

    flash("Student added successfully!", "success")
    return redirect(url_for("home"))


# -----------------------------------
# EDIT STUDENT: DISPLAY FORM
# -----------------------------------

@app.route("/edit/<int:id>", methods=["GET"])
def edit_page(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (id,)
        )
        student = cursor.fetchone()

    finally:
        cursor.close()
        connection.close()

    if student is None:
        flash("Student record not found.", "error")
        return redirect(url_for("home"))

    return render_template("edit_student.html", student=student)
# -----------------------------------
# UPDATE STUDENT
# -----------------------------------

@app.route("/update/<int:id>", methods=["POST"])
def update_student(id):

    student, error = validate_student_form()

    if error:
        flash(error, "error")
        return redirect(url_for("edit_page", id=id))

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE students
            SET name = %s, age = %s, subject = %s
            WHERE id = %s
            """,
            (
                student["name"],
                student["age"],
                student["subject"],
                id
            )
        )

        connection.commit()

        if cursor.rowcount == 0:
            flash("Student record not found or no changes were made.", "error")
            return redirect(url_for("home"))

    finally:
        cursor.close()
        connection.close()

    flash("Student record updated successfully!", "success")
    return redirect(url_for("home"))


# -----------------------------------
# DELETE STUDENT
# -----------------------------------

@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (id,)
        )

        deleted = cursor.rowcount
        connection.commit()

    finally:
        cursor.close()
        connection.close()

    if deleted:
        flash("Student deleted successfully!", "success")
    else:
        flash("Student record not found.", "error")

    return redirect(url_for("home"))
# -----------------------------------
# RUN FLASK APPLICATION
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)
