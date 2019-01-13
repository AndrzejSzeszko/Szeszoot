from django.shortcuts import (
    redirect,
)
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
    ListView,
    DetailView,
    View,
)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    SignInForm,
    QuizForm,
    QuestionAnswerForm,
    PlayerForm,
)
from .models import (
    Quiz,
    Game,
    Player,
)
from .serializers import (
    QuizSerializer,
)
from random import shuffle


class HomeView(TemplateView):
    template_name = 'app_szeszoot/home.html'


class SignInView(CreateView):
    model         = get_user_model()
    template_name = 'app_szeszoot/sign_up.html'
    form_class    = SignInForm
    success_url   = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, f'User {self.object} has been successfully created!')
        return super().form_valid(form)


class AddQuizView(LoginRequiredMixin, FormView):
    template_name = 'app_szeszoot/quiz_add.html'
    form_class    = QuizForm

    def get_success_url(self, *args):
        return reverse_lazy('question-create', kwargs={
            'quiz_title': self.request.POST['title']
        })


class QuestionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app_szeszoot/question_create.html'
    form_class    = QuestionAnswerForm
    pk_url_kwarg  = 'quiz_title'

    def get_success_url(self):
        return reverse_lazy('question-create', kwargs={'quiz_title': self.kwargs['quiz_title']})

    def form_valid(self, form):
        question      = form['question'].save(commit=False)
        question.quiz = Quiz.objects.get_or_create(title=self.kwargs['quiz_title'])[0]
        question.save()
        for name, subform in form.forms.items():
            if 'answer' in name:
                answer            = subform.save(commit=False)
                answer.question   = question
                answer.is_correct = (name == 'answer1')
                answer.save()
        messages.success(self.request, 'Previous question successfully saved!')
        return redirect(self.get_success_url())


class QuizListView(LoginRequiredMixin, ListView):
    model         = Quiz
    template_name = 'app_szeszoot/quiz_list.html'


class GameCreateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        game = Game.objects.create(quiz=Quiz.objects.get(pk=self.kwargs['quiz_pk']))
        return redirect(reverse_lazy('game-master-panel', kwargs={
            'game_pk': game.pk,
        }))


class GameMasterPanelView(LoginRequiredMixin, DetailView):
    model         = Game
    template_name = 'app_szeszoot/game_master_panel.html'
    pk_url_kwarg  = 'game_pk'

    def get_context_data(self, **kwargs):
        ctx         = super().get_context_data(**kwargs)
        quiz_dict = QuizSerializer(self.object.quiz).data

        for question in quiz_dict['question_set']:
            shuffle(question['answer_set'])

        ctx['quiz_dict'] = quiz_dict
        return ctx


class PlayerCreateView(CreateView):
    model         = Player
    form_class    = PlayerForm
    template_name = 'app_szeszoot/player_create.html'

    def get_success_url(self):
        return reverse_lazy('player-panel', kwargs={
            'pk': self.object.id,
        })


class PlayerPanelView(DetailView):
    model = Player
    template_name = 'app_szeszoot/player_panel.html'
