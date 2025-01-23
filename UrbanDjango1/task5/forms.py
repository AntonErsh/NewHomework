from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, label='Введите логин')
    password = forms.CharField(min_length=8, label='Введите пароль')
    repeat_password = forms.CharField(min_length=8, label="Повторите пароль")
    age = forms.CharField(max_length=3, label='Введите свой возраст')


def is_valid_data(username: str, password, repeat_password, age: str, users: list[str], info: dict) -> bool:

    if password == repeat_password and age >= '18' and username not in users:
        return True

    elif password != repeat_password:
        info.update({'error': 'Пароли не совпадают'})
        return False

    elif age < '18':
        info.update({'error': 'Вы должны быть старше 18'})
        return False

    elif username in users:
        info.update({'error': 'Пользователь уже существует'})
        return False
