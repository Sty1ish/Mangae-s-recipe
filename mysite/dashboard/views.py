from django.shortcuts import render
from django.http import HttpResponse 
from . import models

# Create your views here.
def index(request):
    latest_question_list = models.Recipe.objects.all()[0]
    context = {'recipe': latest_question_list}
    return render(request, 'index.html', context)
    