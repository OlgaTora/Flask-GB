import random

from flask import Flask, render_template
from Seminar_3.task_1.models import db, Student, Faculty

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("OK")


@app.cli.command("fill-db")
def fill_tables():
    count_students = 5
    count_faculty = 3
    for faculty in range(1, count_faculty + 1):
        new_faculty = Faculty(name=f"faculty{faculty}")
        db.session.add(new_faculty)

    for student in range(1, count_students + 1):
        new_student = Student(
            name=f"name{student}",
            surname=f"surname{student}",
            age=random.randint(18, 25),
            gender=random.choice(["male", "female"]),
            group=f"group{student}",
            faculty_id=random.randint(1, 3),
        )
        db.session.add(new_student)
    db.session.commit()


@app.route("/students/")
def all_students():
    students = Student.query.all()
    context = {"students": students}
    return render_template("students.html", **context)
