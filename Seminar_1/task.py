"""
1. Напишите простое веб-приложение на Flask, которое будет
выводить на экран текст "Hello, World!".
2. Добавьте две дополнительные страницы в ваше веб-
приложение: страницу "about", страницу "contact".
3. Написать функцию, которая будет принимать на вход два
числа и выводить на экран их сумму.
4. Написать функцию, которая будет принимать на вход строку и
выводить на экран ее длину.
5. Написать функцию, которая будет выводить на экран HTML
страницу с заголовком "Моя первая HTML страница" и
абзацем "Привет, мир!".
6. Написать функцию, которая будет выводить на экран HTML
страницу с таблицей, содержащей информацию о студентах.
Таблица должна содержать следующие поля: "Имя",
"Фамилия", "Возраст", "Средний балл".
Данные о студентах должны быть переданы в шаблон через
контекст.
7. Написать функцию, которая будет выводить на экран HTML
страницу с блоками новостей.
Каждый блок должен содержать заголовок новости,
краткое описание и дату публикации.
Данные о новостях должны быть переданы в шаблон через контекст.
"""
from datetime import datetime

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/about/')
def about():
    return 'About'


@app.route('/contact/')
def contact():
    return 'Contact'


@app.route('/<int:a>/<int:b>/')
def sum_nums(a: int, b: int) -> str:
    return str(a + b)


@app.route('/<string:s>/')
def string_length(s: str):
    return str(len(s))


@app.route('/hello/')
def my_first_page():
    return render_template('hello.html')


@app.route('/students/')
def students():
    head = {
        'firstname': 'Имя',
        'lastname': 'Фамилия',
        'age': 'Возраст',
        'rating': 'Средний балл'
    }

    students_list = [
        {
            'firstname': 'Иван',
            'lastname': 'Иванов',
            'age': 18,
            'rating': 4
        },
        {
            'firstname': 'Петр',
            'lastname': 'Петров',
            'age': 19,
            'rating': 3
        },
        {
            'firstname': 'Семен',
            'lastname': 'Семенов',
            'age': 20,
            'rating': 5
        }]

    return render_template('students.html', **head, students_list=students_list)


@app.route('/news/')
def news():
    news_block = [
        {
            'title': 'новость_1',
            'description': 'описание_1',
            'create_at': datetime.now().strftime('%H:%M - %m.%d.%Y года')
        },
        {
            'title': 'новость_2',
            'description': 'описание_2',
            'create_at': datetime.now().strftime('%H:%M - %m.%d.%Y года')
        },
        {
            'title': 'новость_3',
            'description': 'описание_3',
            'create_at': datetime.now().strftime('%H:%M - %m.%d.%Y года')
        }]
    return render_template('news.html', news_block=news_block)


if __name__ == '__main__':
    app.run()
