from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse,Http404
from django.template import loader

from .models import Question

# Create your views here.


def index(request):

    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = "<br/> ".join([q.question_text for q in latest_question_list])
    
    latest_question_list = get_list_or_404(Question.objects.order_by("-pub_date"))[:5]

    template = loader.get_template('polls/index.html')

    context = {
        'latest_question_list':latest_question_list
    }
    output = template.render(context, request)

    return HttpResponse(output)
    
def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}

    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    template = loader.get_template("polls/results.html")

    question = get_object_or_404(Question,pk=question_id)

    context = {
        'question':question
    }
    output = template.render(context, request)

    return HttpResponse(output)

def vote(request, question_id):

    """ question = get_object_or_404(Question, pk=question_id)


    template = loader.get_template("polls/vote.html")
    context = {
        'question':question
    }
    
    
    output = template.render(context, request)

    return HttpResponse(output) """
    question = get_o



