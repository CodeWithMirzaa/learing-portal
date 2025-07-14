from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
     path('upload-video/', views.upload_video_view_test, name='upload_video'),
     path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
     path('quiz/<int:video_id>/', views.quiz_view, name='quiz'),
    

]
