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

# These handlers must be placed in the root URLconf (e_learning/urls.py)
# to take effect. They are defined here for reference.
handler404 = 'edukimi_femijeve.views.custom_404'
handler500 = 'edukimi_femijeve.views.custom_500'
