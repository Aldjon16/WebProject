from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Course


class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Regjistrimi u krye me sukses.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
