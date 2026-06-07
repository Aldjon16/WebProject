"""
Unit tests for the edukimi_femijeve Django app.

Covers: models (Course, Student, Enrollment), views (CourseListView,
CourseDetailView, register), URL routing, and admin registration.
"""

from django.contrib.admin.sites import site as admin_site
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.utils import timezone

from edukimi_femijeve.models import Course, Student, Enrollment
from edukimi_femijeve.views import CourseDetailView, CourseListView, register


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class CourseModelTests(TestCase):
    """Tests for the Course model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="instructor", password="testpass123"
        )
        self.course = Course.objects.create(
            title="Python Basics",
            description="Intro to Python",
            category="programim",
            level="fillestar",
            duration=10,
            instructor=self.user,
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.course), "Python Basics")

    def test_default_ordering_is_newest_first(self):
        older = Course.objects.create(
            title="Older Course",
            description="Old",
            category="design",
            level="mesatar",
            duration=5,
            instructor=self.user,
            created_at=timezone.now() - timezone.timedelta(days=10),
        )
        courses = list(Course.objects.all())
        self.assertEqual(courses[0], self.course)
        self.assertEqual(courses[1], older)

    def test_category_choices(self):
        expected_keys = {"programim", "design", "business"}
        actual_keys = {key for key, _ in Course.CATEGORY_CHOICES}
        self.assertEqual(actual_keys, expected_keys)

    def test_level_choices(self):
        expected_keys = {"fillestar", "mesatar", "avancuar"}
        actual_keys = {key for key, _ in Course.LEVEL_CHOICES}
        self.assertEqual(actual_keys, expected_keys)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.course.created_at)

    def test_updated_at_changes_on_save(self):
        old_updated = self.course.updated_at
        self.course.title = "Python Advanced"
        self.course.save()
        self.course.refresh_from_db()
        self.assertGreaterEqual(self.course.updated_at, old_updated)

    def test_image_field_blank_and_null(self):
        self.assertIsNone(self.course.image.name)

    def test_instructor_related_name(self):
        self.assertIn(self.course, self.user.courses.all())

    def test_duration_positive_integer(self):
        self.assertGreater(self.course.duration, 0)


class StudentModelTests(TestCase):
    """Tests for the Student model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="student1", password="testpass123"
        )
        self.student = Student.objects.create(
            user=self.user, name="Aldjon", surname="Kacollja"
        )

    def test_str_returns_full_name(self):
        self.assertEqual(str(self.student), "Aldjon Kacollja")

    def test_user_one_to_one(self):
        self.assertEqual(self.student.user, self.user)

    def test_user_can_be_null(self):
        anon = Student.objects.create(name="Anon", surname="Student")
        self.assertIsNone(anon.user)

    def test_enrolled_courses_empty_by_default(self):
        self.assertEqual(self.student.enrolled_courses.count(), 0)


class EnrollmentModelTests(TestCase):
    """Tests for the Enrollment model."""

    def setUp(self):
        self.instructor = User.objects.create_user(
            username="instructor", password="testpass123"
        )
        self.course = Course.objects.create(
            title="Design 101",
            description="Learn design",
            category="design",
            level="fillestar",
            duration=8,
            instructor=self.instructor,
        )
        self.student = Student.objects.create(name="Eneriko", surname="Troka")
        self.enrollment = Enrollment.objects.create(
            student=self.student, course=self.course
        )

    def test_str_returns_student_dash_course(self):
        self.assertEqual(
            str(self.enrollment), "Eneriko Troka - Design 101"
        )

    def test_defaults(self):
        self.assertFalse(self.enrollment.completed)
        self.assertEqual(self.enrollment.progress, 0)

    def test_date_enrolled_auto_set(self):
        self.assertIsNotNone(self.enrollment.date_enrolled)

    def test_unique_together_constraint(self):
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(
                student=self.student, course=self.course
            )

    def test_enrolled_courses_through_enrollment(self):
        self.assertIn(self.course, self.student.enrolled_courses.all())

    def test_cascade_delete_student(self):
        self.student.delete()
        self.assertEqual(Enrollment.objects.count(), 0)

    def test_cascade_delete_course(self):
        self.course.delete()
        self.assertEqual(Enrollment.objects.count(), 0)

    def test_progress_update(self):
        self.enrollment.progress = 75
        self.enrollment.completed = True
        self.enrollment.save()
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.progress, 75)
        self.assertTrue(self.enrollment.completed)


# ---------------------------------------------------------------------------
# View tests
# ---------------------------------------------------------------------------


class CourseListViewTests(TestCase):
    """Tests for the CourseListView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="instructor", password="testpass123"
        )

    def test_empty_list(self):
        response = self.client.get(reverse("course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["courses"], [])

    def test_lists_courses(self):
        c = Course.objects.create(
            title="Web Dev",
            description="Web",
            category="programim",
            level="mesatar",
            duration=12,
            instructor=self.user,
        )
        response = self.client.get(reverse("course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(c, response.context["courses"])

    def test_uses_correct_template(self):
        response = self.client.get(reverse("course_list"))
        self.assertTemplateUsed(response, "course_list.html")


class CourseDetailViewTests(TestCase):
    """Tests for the CourseDetailView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="instructor", password="testpass123"
        )
        self.course = Course.objects.create(
            title="Business 101",
            description="Business basics",
            category="business",
            level="avancuar",
            duration=20,
            instructor=self.user,
        )

    def test_detail_page_status(self):
        url = reverse("course_detail", args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_context_contains_course(self):
        url = reverse("course_detail", args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.context["course"], self.course)

    def test_detail_uses_correct_template(self):
        url = reverse("course_detail", args=[self.course.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "course_detail.html")

    def test_detail_404_for_nonexistent(self):
        url = reverse("course_detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RegisterViewTests(TestCase):
    """Tests for the register function-based view."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("register")

    def test_get_register_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertIn("form", response.context)

    def test_register_valid_user(self):
        data = {
            "username": "newuser",
            "password1": "ComplexPass!99",
            "password2": "ComplexPass!99",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_redirects_to_login(self):
        data = {
            "username": "newuser2",
            "password1": "ComplexPass!99",
            "password2": "ComplexPass!99",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response, reverse("login"), fetch_redirect_response=False
        )

    def test_register_invalid_passwords_mismatch(self):
        data = {
            "username": "baduser",
            "password1": "ComplexPass!99",
            "password2": "WrongPass!99",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="baduser").exists())

    def test_register_duplicate_username(self):
        User.objects.create_user(username="existing", password="test12345")
        data = {
            "username": "existing",
            "password1": "ComplexPass!99",
            "password2": "ComplexPass!99",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="existing").count(), 1)


# ---------------------------------------------------------------------------
# URL tests
# ---------------------------------------------------------------------------


class URLTests(TestCase):
    """Tests for URL routing and resolution."""

    def test_course_list_url_resolves(self):
        resolver = resolve("/")
        self.assertEqual(resolver.func.view_class, CourseListView)

    def test_course_detail_url_resolves(self):
        resolver = resolve("/course/1/")
        self.assertEqual(resolver.func.view_class, CourseDetailView)

    def test_register_url_resolves(self):
        resolver = resolve("/register/")
        self.assertEqual(resolver.func, register)

    def test_login_url_resolves(self):
        resolver = resolve("/login/")
        self.assertEqual(resolver.func.view_class.__name__, "LoginView")

    def test_logout_url_resolves(self):
        resolver = resolve("/logout/")
        self.assertEqual(resolver.func.view_class.__name__, "LogoutView")

    def test_reverse_course_list(self):
        self.assertEqual(reverse("course_list"), "/")

    def test_reverse_course_detail(self):
        self.assertEqual(reverse("course_detail", args=[42]), "/course/42/")

    def test_reverse_register(self):
        self.assertEqual(reverse("register"), "/register/")


# ---------------------------------------------------------------------------
# Admin tests
# ---------------------------------------------------------------------------


class AdminRegistrationTests(TestCase):
    """Tests that all app models are registered with the Django admin."""

    def test_course_registered(self):
        self.assertIn(Course, admin_site._registry)

    def test_student_registered(self):
        self.assertIn(Student, admin_site._registry)

    def test_enrollment_registered(self):
        self.assertIn(Enrollment, admin_site._registry)
