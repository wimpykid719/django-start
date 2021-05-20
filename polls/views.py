from django.shortcuts import render, get_object_or_404
# from django.template import context, loader
from django.http import HttpResponseRedirect
from django.template import context
from .models import Choice, Question
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # テンプレート側でQuestion.objects.order_by('-pub_date')[:5]を呼び出す際の名前を設定している。
    context_object_name = 'Latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

# 汎用リファクタリング前
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

class DetailView(generic.DetailView):
    # テンプレートで変数にアクセスする際はquestionになる。
    model = Question
    template_name = 'polls/detail.html'


# def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    # return render(request, 'polls/detail.html', {'question': question})

    # 汎用リファクタリング前
    # 上記を書き換える。
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# 汎用リファクタリング前
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))