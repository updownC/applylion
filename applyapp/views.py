from django.shortcuts import render, redirect
from .models import User, Question
from .forms import UserCreationForm, UserQuestionForm, SignInForm
from django.contrib import auth, messages
from django.template import RequestContext
from django.http import HttpResponse
# Create your views here.


def index(request):
    messages.info(
        request, '지원 마감 되었습니다.')
    return render(request, 'index.html')


def complete(request):
    return render(request, 'complete.html')


def info(request):
    return render(request, 'info.html')


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            # html = '<div style="display: flex;flex-direction: column;justify-content: center;align-items: center;height: 700px;"><h1>로그인 실패. 다시 시도해보세요</h1><p>존재하지 않는 아이디거나, 비밀번호 오류일 수 있습니다.</p></div>'
            return render(request, 'loginerror.html')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            auth.login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def question(request):
    if request.method == 'POST':
        form = UserQuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('complete')
    else:
        form = UserQuestionForm()
    return render(request, 'question.html', {'form': form})


def questionEdit(request, user_id):
    question = Question.objects.get(user_id=user_id)
    if request.method == 'POST':
        form = UserQuestionForm(request.POST, instance=question)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('complete')
    else:
        form = UserQuestionForm(instance=question)
    return render(request, 'question.html', {'form': form})
