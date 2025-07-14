from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from main.models import Choice, Product, UserProductProgress, Video
from .forms import QuizForm, RegisterForm, VideoForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required



def landing(request):
    return render(request, 'landing.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def dashboard(request):
    products = Product.objects.all()
    completed_products = UserProductProgress.objects.filter(user=request.user, completed=True).values_list('product_id', flat=True)
    return render(request, 'dashboard.html', {
        'products': products,
        'completed_products': completed_products,
    })


@staff_member_required
def upload_video_view_test(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})

@login_required
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def quiz_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    questions = video.questions.prefetch_related('choices')

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected:
                choice = Choice.objects.get(id=selected)
                if choice.is_correct:
                    score += 1

        # If passed, redirect to next video or dashboard
        next_video = Video.objects.filter(product=video.product, order__gt=video.order).order_by('order').first()
        if next_video:
            return redirect('product_detail', pk=video.product.pk)  # or create a dedicated video view
        else:
            return redirect('dashboard')  # mark product as completed if needed

    return render(request, 'quiz.html', {
        'video': video,
        'questions': questions,
    })


@login_required
def quiz_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    questions = video.questions.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            total = questions.count()

            for question in questions:
                selected = form.cleaned_data.get(f'question_{question.id}')
                if selected == question.correct_option:
                    score += 1

            # You can store result if needed — for now just use messages
            messages.success(request, f'You scored {score}/{total}')

            # Check for next video in order
            next_video = Video.objects.filter(
                product=video.product,
                order__gt=video.order
            ).order_by('order').first()

            if next_video:
                return redirect('product_detail', product_id=video.product.id)
            else:
                # Mark product as completed
                UserProductProgress.objects.update_or_create(
                    user=request.user,
                    product=video.product,
                    defaults={'completed': True}
                )
                return redirect('dashboard')

    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz.html', {'form': form, 'video': video})