from django.shortcuts import (
    render,
    redirect,
)
from django.utils.safestring import mark_safe
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    FormView,
    ListView,
    DetailView,
    View,
)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
import json
from .forms import (
    SignInForm,
    QuizForm,
    QuestionForm,
    AnswerForm,
    QuestionAnswerForm,
    PlayerForm,
)
from .models import (
    Quiz,
    Question,
    Answer,
    Game,
    Player,
)


def index(request):
    return render(request, 'app_szeszoot/index.html', {})


def room(request, room_name):
    return render(request, 'app_szeszoot/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
    })


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


class AddQuizView(FormView):
    template_name = 'app_szeszoot/quiz_add.html'
    form_class    = QuizForm

    def get_success_url(self):
        return reverse_lazy('question-create', kwargs={'quiz_title': self.request.POST['title']})


class QuestionCreateView(CreateView):
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


class QuizListView(ListView):
    model         = Quiz
    template_name = 'app_szeszoot/quiz_list.html'


class GameCreateView(View):
    def get(self, *args, **kwargs):
        game = Game.objects.create()
        return redirect(reverse_lazy('game-master-panel', kwargs={
            'game_pk': game.id,
            'quiz_pk': self.kwargs['quiz_pk'],
        }))


class GameMasterPanelView(DetailView):
    model         = Quiz
    template_name = 'app_szeszoot/game_master_panel.html'
    pk_url_kwarg  = 'quiz_pk'

    def get_context_data(self, **kwargs):
        ctx         = super().get_context_data(**kwargs)
        ctx['game'] = Game.objects.get(pk=self.kwargs.get('game_pk'))
        return ctx


class PlayerCreateView(CreateView):
    model         = Player
    form_class    = PlayerForm
    template_name = 'app_szeszoot/player_create.html'

    def get_success_url(self):
        return reverse_lazy('game', kwargs={'pk': self.request.POST['game']})


class GameView(DetailView):
    model = Game
    template_name = 'app_szeszoot/game.html'
