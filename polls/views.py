from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):

        now = timezone.now()


        return Question.objects.filter(
            pub_date__lte = now
        ).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    template_name="polls/detail.html"
    model = Question

    def get_queryset(self):

        now = timezone.now()

        return Question.objects.filter(pub_date__lte = now)


    
class ResultsView(generic.DetailView):
    template_name="polls/results.html"
    model = Question


    def get_queryset(self):
        now = timezone.now()

        return Question.objects.filter(pub_date__lte = now)

def vote(request, question_id):

    

    question = get_object_or_404(Question, pk=question_id)  
    try:
        
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        
    except(KeyError, Choice.DoesNotExist):

        error = {
            "question":question,
            "error_message":"You didn't select any choice"
        }

        return render(request, "polls/details.html", error)

    else:
        selected_choice.votes += 1
        selected_choice.save()

        

        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))



