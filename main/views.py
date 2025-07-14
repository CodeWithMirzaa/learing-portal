from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import RegisterForm, VideoForm, QuizForm
from .models import Product, Video, QuizQuestion, Choice, UserProductProgress, QuizSubmission


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
    completed_products = UserProductProgress.objects.filter(
        user=request.user,
        completed=True
    ).values_list('product_id', flat=True)
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

            # Save quiz submission
            QuizSubmission.objects.update_or_create(
                user=request.user,
                video=video,
                defaults={'score': score}
            )

            messages.success(request, f'You scored {score}/{total}')

            # Check if all video quizzes are completed
            all_videos = video.product.videos.all()
            all_done = all(
                QuizSubmission.objects.filter(user=request.user, video=v).exists()
                for v in all_videos
            )

            if all_done:
                UserProductProgress.objects.update_or_create(
                    user=request.user,
                    product=video.product,
                    defaults={'completed': True}
                )

            # Redirect to next video or dashboard
            next_video = Video.objects.filter(
                product=video.product,
                order__gt=video.order
            ).order_by('order').first()

            if next_video:
                return redirect('product_detail', pk=video.product.id)
            else:
                return redirect('dashboard')
    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz.html', {'form': form, 'video': video})

@login_required
def quiz_results_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    videos = product.videos.all()

    results = []
    for video in videos:
        submission = QuizSubmission.objects.filter(user=request.user, video=video).first()
        results.append({
            'video': video,
            'score': submission.score if submission else None,
            'submitted': submission is not None
        })

    return render(request, 'quiz_results.html', {
        'product': product,
        'results': results
    })
