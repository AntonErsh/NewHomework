from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
def def_view(request):
    return render(request, 'def_view.html')


class ClassView(TemplateView):
    template_name = 'class_view.html'


def start(request):
    return render(request, 'second_task/start.html')
