import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Course

logger = logging.getLogger(__name__)


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
            try:
                form.save()
            except IntegrityError:
                logger.exception("Failed to save new user")
                messages.error(request, 'Gabim gjatë regjistrimit. Ju lutem provoni përsëri.')
                return render(request, 'register.html', {'form': form})
            messages.success(request, 'Regjistrimi u krye me sukses.')
            return redirect('login')
        else:
            messages.error(request, 'Regjistrimi dështoi. Ju lutem korrigjoni gabimet më poshtë.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)
