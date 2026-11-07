from flask import Flask, request, jsonify, render_template
from restdb import get_connection
import mysql.connector

app = Flask(__name__)


# HOME
@app.route("/")
def home():

    return jsonify({
        "message": "REST School API is running!",
        "dashboard": "/dashboard",
        "students_api": "/api/students"
    })


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    return render_template("restdashboard.html")


# GET ALL STUDENTS
@app.route("/api/students", methods=["GET"])
def get_students():

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM reststudent ORDER BY id DESC"
        )

        students = cursor.fetchall()

        return jsonify({
            "students": students,
            "total": len(students)
        }), 200

    except mysql.connector.Error:
        app.logger.exception("GET STUDENTS ERROR")
        return jsonify({"error": "Unable to retrieve students"}), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# GET ONE STUDENT
@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM reststudent WHERE id = %s",
            (id,)
        )

        student = cursor.fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"student": student}), 200

    except mysql.connector.Error:
        app.logger.exception("GET STUDENT ERROR")
        return jsonify({"error": "Unable to retrieve student"}), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ADD STUDENT
@app.route("/api/students", methods=["POST"])
def add_student():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON data"}), 400

    name = data.get("name")
    subject = data.get("subject")
    age = data.get("age")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Student name is required"}), 400

    if not isinstance(subject, str) or not subject.strip():
        return jsonify({"error": "Subject is required"}), 400

    if isinstance(age, bool):
        return jsonify({"error": "Enter a valid age"}), 400

    try:
        age = int(age)

        if age < 1 or age > 120:
            return jsonify({"error": "Age must be between 1 and 120"}), 400

    except (ValueError, TypeError):
        return jsonify({"error": "Age must be a valid number"}), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO reststudent (name, age, subject)
            VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (name.strip(), age, subject.strip()))
        conn.commit()

        return jsonify({
            "message": "Student added successfully!",
            "student_id": cursor.lastrowid
        }), 201

    except mysql.connector.Error:
        if conn:
            conn.rollback()

        app.logger.exception("ADD STUDENT ERROR")
        return jsonify({"error": "Database error: unable to add student"}), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# UPDATE STUDENT
@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON data"}), 400

    name = data.get("name")
    subject = data.get("subject")
    age = data.get("age")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Student name is required"}), 400

    if not isinstance(subject, str) or not subject.strip():
        return jsonify({"error": "Subject is required"}), 400

    if isinstance(age, bool):
        return jsonify({"error": "Enter a valid age"}), 400

    try:
        age = int(age)

        if age < 1 or age > 120:
            return jsonify({"error": "Age must be between 1 and 120"}), 400

    except (ValueError, TypeError):
        return jsonify({"error": "Enter a valid age"}), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM reststudent WHERE id = %s",
            (id,)
        )

        if cursor.fetchone() is None:
            return jsonify({"error": "Student not found"}), 404

        sql = """
            UPDATE reststudent
            SET name = %s, age = %s, subject = %s
            WHERE id = %s
        """

        cursor.execute(
            sql,
            (name.strip(), age, subject.strip(), id)
        )

        conn.commit()

        return jsonify({
            "message": "Student updated successfully!"
        }), 200

    except mysql.connector.Error:
        if conn:
            conn.rollback()

        app.logger.exception("UPDATE STUDENT ERROR")
        return jsonify({"error": "Unable to update student"}), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# DELETE STUDENT
@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM reststudent WHERE id = %s",
            (id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404

        conn.commit()

        return jsonify({
            "message": "Student deleted successfully!"
        }), 200

    except mysql.connector.Error:
        if conn:
            conn.rollback()

        app.logger.exception("DELETE STUDENT ERROR")
        return jsonify({"error": "Unable to delete student"}), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )