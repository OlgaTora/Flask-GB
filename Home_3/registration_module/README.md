Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
содержать следующие поля:
Имя пользователя (обязательное поле)
Фамилия пользователя (обязательное поле)
Электронная почта (обязательное поле, с валидацией на корректность ввода email)
Поле пароль должно содержать не менее 8 символов, включая хотя бы одну букву и
одну цифру(обязательное поле, с валидацией на минимальную длину пароля)
Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
дата рождения (обязательное поле, с валидацией)
согласие на обработку персональных данных (обязательное поле).

Форма должна содержать кнопку "Зарегистрироваться".

После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации.

Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.

Пароль должен быть зашифрован

Добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке.