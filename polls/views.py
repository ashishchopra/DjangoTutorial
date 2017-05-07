from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question, Choice
# from django.template import loader
# from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'q_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lt=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def index(request):
#     q_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     context = {
#         'q_list': q_list
#     }
#     # output = ', '.join([q.question_text for q in q_list])
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     q = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': q})


# def results(request, question_id):
#     q = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': q})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question,
                      'error_message': 'You did not select a choice.'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                    args=(question.id,)))
