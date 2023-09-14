from pathlib import PurePath, Path

from flask import Flask, render_template, request, redirect, url_for, abort, flash
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/")
def base():
    return render_template("base.html")


@app.get("/next/")
def next_page():
    return "Hello, Baby"


@app.route("/load_pic/", methods=["GET", "POST"])
def load_pic():
    context = {"task": "Task 2"}
    if request.method == "POST":
        file = request.files.get("file")
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), "uploads", file_name))
        return f"Your pic {escape(file_name)} has load"
    return render_template("load_pic.html", **context)


@app.route("/login/", methods=["POST", "GET"])
def login():
    context = {"task": "Task 3"}
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if is_correct_data(name, password):
            return f"Authorization successfully, {escape(name)}"
        else:
            return redirect(url_for("failed_log"))
    return render_template("login.html", **context)


def is_correct_data(name: str, password: str) -> bool:
    user1 = {"login": "Ivan", "password": "123"}
    if name == user1.get("login") and password == user1.get("password"):
        return True
    return False


@app.route("/failed_log/")
def failed_log():
    return render_template("failed_log.html")


@app.route("/text/", methods=["POST", "GET"])
def text():
    context = {"task": "Task 4"}
    if request.method == "POST":
        input_text = request.form.get("text")
        result = len(input_text.split())
        return f"Your text have {result} words"
    return render_template("text.html", **context)


@app.route("/math/", methods=["POST", "GET"])
def math():
    context = {"task": "Task 5"}
    if request.method == "POST":
        a = int(request.form.get("number_1"))
        b = int(request.form.get("number_2"))
        oper = request.form.get("oper")
        match oper:
            case "+":
                result = a + b
            case "-":
                result = a - b
            case "/":
                if b == 0:
                    return "Zero division is not possible"
                result = a / b
            case "*":
                result = a * b
        return f"Result of {a}{oper}{b} = {result}"
    return render_template("math.html", **context)


@app.route("/age/", methods=["POST", "GET"])
def check_age():
    min_age = 18
    context = {"task": "Task 6"}
    if request.method == "POST":
        name = request.form.get("name")
        age = int(request.form.get("age"))
        if age > min_age:
            return f"Welcome, {name}"
        abort(403)
    return render_template("age.html", **context)


@app.errorhandler(403)
def page_not_found(e):
    context = {"title": "Access not permitted", "url": request.base_url}
    return render_template("403.html", **context), 403


@app.route("/square/", methods=["POST", "GET"])
def square():
    context = {"task": "Task 7"}
    if request.method == "POST":
        number = int(request.form.get("number"))
        return redirect(url_for("square_result", number=number))
    return render_template("square.html", **context)


@app.route("/square_result/<int:number>")
def square_result(number: int):
    return render_template("square_result.html", number=number)


app.secret_key = b"5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4"


@app.route("/form", methods=["GET", "POST"])
def form():
    context = {"task": "Task 8"}
    if request.method == "POST":
        if not request.form["name"]:
            flash("Введите имя!", "danger")
            return redirect(url_for("form"))
        flash("Форма успешно отправлена!", "success")
        return redirect(url_for("form"))
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
