from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import CSRFProtect
from Home_3.registration_module.models import db, User
from Home_3.registration_module.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "cc1a72c6a9c3a2a6ee88614f773c6f89e8011f7699073efe09f513186ebc6302"
csrf = CSRFProtect(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:////home/olgatorres/PycharmProjects/Flask/Home_3/registration_module/instance/users.db"
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("hello", username=f'{session["username"]}'))
    else:
        return render_template("index.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        session["username"] = request.form.get("username") or "NoName"
        username = form.username.data
        surname = form.surname.data
        email = form.email.data
        birthday = form.birthday.data
        confirm = form.confirm.data
        password = form.password.data
        if is_exist(username):
            message = "Name is already exist"
            form.username.errors.append(message)
            return render_template("register.html", form=form)
        add_user(
            username,
            surname,
            email,
            birthday,
            confirm,
            generate_password_hash(password),
        )
        return redirect(url_for("hello", username=username))
    return render_template("register.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("hello", username=f'{session["username"]}'))
    else:
        form = LoginForm()
        if request.method == "POST" and form.validate():
            session["username"] = request.form.get("username") or "NoName"
            username = form.username.data
            password = form.password.data
            if check_login(username, password):
                return redirect(url_for("hello", username=username))
            else:
                message = "Wrong name or password. Try again!"
                form.username.errors.append(message)
                session.pop("username", None)
                return render_template("login.html", form=form)
        return render_template("login.html", form=form)


@app.route("/hello/<string:username>", methods=["GET", "POST"])
def hello(username):
    return render_template("hello.html", username=username)


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("index"))


def add_user(
    username: str, surname: str, email: str, birthday: str, confirm: str, password: str
):
    user = User(
        username=username,
        surname=surname,
        email=email,
        birthday=birthday,
        confirm=confirm,
        password=password,
    )
    db.session.add(user)
    db.session.commit()


def is_exist(username: str) -> bool:
    user = User.query.filter(User.username == username).first()
    return True if user else False


def check_login(username: str, password: str):
    user = User.query.filter(User.username == username).first()
    if user:
        return check_password_hash(user.password, password)
    else:
        return False


@app.route("/users/")
def show_users():
    users = User.query.all()
    context = {"users": users}
    return render_template("users.html", **context)
