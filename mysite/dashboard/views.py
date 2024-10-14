from django.shortcuts import render
from django.http import HttpResponse 
# Create your views here.
def index(request):
    # latest_question_list = models.Question.objects.order_by('-pub_date')[:5]
    # context = {'questions': latest_question_list}
    # #context = {'questions': []}
    # return render(request, 'polls/index.html', context)
    return HttpResponse('Hello')