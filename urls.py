from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CourseListView, CourseDetailView, register

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),

    path('register/', register, name='register'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
