from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegistrationForm, is_valid_data
# Create your views here.


def sign_up_by_html(request):
    users = ['Ivan', 'Boris220', 'NikolaMango', 'JackBack', 'Botinok199']
    info = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')

        if is_valid_data(username, password, repeat_password, age, users, info):
            return HttpResponse(f'Приветствуем, {username}!')
        else:
            return render(request, 'fifth_task/registration_page.html', info)

    return render(request, 'fifth_task/registration_page.html', info)


def sign_up_by_django(request):
    users = ['Ivan', 'Boris220', 'NikolaMango', 'JackBack', 'Botinok199']
    info = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if is_valid_data(username, password, repeat_password, age, users, info):
                return HttpResponse(f'Приветствуем, {username}!')
            else:
                return render(request, 'fifth_task/registration_page.html', info)

    else:
        form = RegistrationForm()
    return render(request, 'fifth_task/registration_page.html', {'form': form})
