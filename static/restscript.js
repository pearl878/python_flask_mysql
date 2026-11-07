const API = "/api/students";

const form = document.getElementById("studentForm");
const table = document.getElementById("studentTable");
const message = document.getElementById("message");

let students = [];


// SHOW MESSAGE
function showMessage(text, error = false) {

    message.textContent = text;
    message.style.color = error ? "#fca5a5" : "#67e8f9";

}


// LOAD STUDENTS
async function loadStudents() {

    try {

        const response = await fetch(API);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to load students");
        }

        students = data.students;

        filterStudents();

    } catch (error) {

        showMessage(error.message, true);

    }

}


// DISPLAY STUDENTS
function displayStudents(data) {

    table.replaceChildren();

    document.getElementById("total").textContent = students.length;

    data.forEach(student => {

        const row = document.createElement("tr");

        [student.id, student.name, student.age, student.subject]
            .forEach(value => {

                const cell = document.createElement("td");

                cell.textContent = value;

                row.appendChild(cell);

            });


        const actions = document.createElement("td");

        const edit = document.createElement("button");

        edit.textContent = "Edit";
        edit.className = "edit";

        edit.onclick = () => editStudent(student);


        const remove = document.createElement("button");

        remove.textContent = "Delete";
        remove.className = "delete";

        remove.onclick = () => deleteStudent(student.id);


        actions.append(edit, remove);

        row.appendChild(actions);

        table.appendChild(row);

    });


    if (data.length === 0) {

        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 5;
        cell.textContent = "No students found.";

        row.appendChild(cell);
        table.appendChild(row);

    }

}
// SEARCH STUDENTS
function filterStudents() {

    const value = document
        .getElementById("search")
        .value
        .toLowerCase();

    const filtered = students.filter(student =>

        student.name.toLowerCase().includes(value) ||
        student.subject.toLowerCase().includes(value)

    );

    displayStudents(filtered);

}


// ADD OR UPDATE STUDENT
form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const id = document.getElementById("studentId").value;

    const student = {

        name: document.getElementById("name").value.trim(),

        age: Number(document.getElementById("age").value),

        subject: document.getElementById("subject").value.trim()

    };


    if (
        !student.name ||
        !student.subject ||
        !Number.isInteger(student.age) ||
        student.age < 1 ||
        student.age > 120
    ) {

        showMessage("Please enter valid student details.", true);

        return;

    }


    const saveBtn = document.getElementById("saveBtn");

    saveBtn.disabled = true;
    saveBtn.textContent = id ? "Updating..." : "Adding...";


    try {

        const response = await fetch(
            id ? `${API}/${id}` : API,
            {

                method: id ? "PUT" : "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(student)

            }
        );


        const result = await response.json();

        if (!response.ok) {

            throw new Error(result.error || "Operation failed");

        }


        showMessage(result.message);

        form.reset();

        resetForm();

        await loadStudents();


    } catch (error) {

        showMessage(error.message, true);

    } finally {

        saveBtn.disabled = false;

        saveBtn.textContent = document
            .getElementById("studentId").value
            ? "Update Student"
            : "Add Student";

    }

});


// EDIT STUDENT
function editStudent(student) {

    document.getElementById("studentId").value = student.id;

    document.getElementById("name").value = student.name;

    document.getElementById("age").value = student.age;

    document.getElementById("subject").value = student.subject;


    document.getElementById("formTitle").textContent = "Update Student";

    document.getElementById("saveBtn").textContent = "Update Student";

    document.getElementById("cancelBtn").hidden = false;


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


// RESET FORM
function resetForm() {

    document.getElementById("studentId").value = "";

    document.getElementById("formTitle").textContent = "Add New Student";

    document.getElementById("saveBtn").textContent = "Add Student";

    document.getElementById("cancelBtn").hidden = true;

}


// CANCEL EDIT
document.getElementById("cancelBtn").addEventListener("click", function() {

    form.reset();

    resetForm();

    showMessage("");

});


// DELETE STUDENT
async function deleteStudent(id) {

    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }

    try {

        const response = await fetch(`${API}/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {

            throw new Error(result.error || "Unable to delete student");

        }

        showMessage(result.message);

        await loadStudents();

    } catch (error) {

        showMessage(error.message, true);

    }

}


// SEARCH EVENT
document.getElementById("search").addEventListener("input", filterStudents);


// START APPLICATION
loadStudents();