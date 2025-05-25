from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subject, Question, Answer, TestResult

def home(request):
    """Bosh sahifani ko'rsatish"""
    subjects = Subject.objects.all()
    return render(request, 'tests/home.html', {'subjects': subjects})

def user_logout(request):
    logout(request)
    return redirect('login')  # Login sahifasiga qaytish

@login_required
def test(request, subject_id):
    """Testni ko'rsatish va natijalarni qayd etish"""
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject).prefetch_related('answer_set')
    
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        
        for question in questions:
            user_answer_id = request.POST.get(f'q{question.id}')
            if user_answer_id:
                try:
                    correct_answer = Answer.objects.get(question=question, is_correct=True)
                    if int(user_answer_id) == correct_answer.id:
                        correct += 1
                except Answer.DoesNotExist:
                    pass
        
        # Natijani bazaga saqlash
        TestResult.objects.create(
            user=request.user,
            subject=subject,
            score=correct,
            total=total
        )
        
        return render(request, 'tests/result.html', {
            'correct': correct,
            'total': total,
            'subject': subject,
            'percentage': round((correct / total) * 100, 2) if total > 0 else 0
        })
    
    return render(request, 'tests/test.html', {
        'subject': subject,
        'questions': questions,
    })

def register(request):
    """Foydalanuvchi registratsiyasi"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'tests/register.html', {'form': form})

@login_required
def profile(request):
    """Foydalanuvchi profili va natijalari"""
    results = TestResult.objects.filter(user=request.user).select_related('subject').order_by('-date')
    return render(request, 'tests/profile.html', {
        'results': results,
        'user': request.user
    })

# Qo'shimcha funksiyalar (agar kerak bo'lsa)
@login_required
def leaderboard(request):
    """Eng yaxshi test yechuvchilar reytingi"""
    top_results = TestResult.objects.all() \
        .select_related('user', 'subject') \
        .order_by('-score')[:10]
    return render(request, 'tests/leaderboard.html', {'results': top_results})

@login_required
def test_history(request):
    """Foydalanuvchining barcha test natijalari"""
    results = TestResult.objects.filter(user=request.user) \
        .select_related('subject') \
        .order_by('-date')
    return render(request, 'tests/history.html', {'results': results})