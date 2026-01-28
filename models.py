from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('programim', 'Programim'),
        ('design', 'Design'),
        ('business', 'Business'),
    ]

    LEVEL_CHOICES = [
        ('fillestar', 'Fillestar'),
        ('mesatar', 'Mesatar'),
        ('avancuar', 'Avancuar'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    duration = models.PositiveIntegerField(help_text="Kohëzgjatja në orë")
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    enrolled_courses = models.ManyToManyField(Course, through='Enrollment')

    def __str__(self):
        return f"{self.name} {self.surname}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student} - {self.course}"