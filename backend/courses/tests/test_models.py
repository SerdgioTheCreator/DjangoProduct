from django.core.exceptions import ValidationError
from django.test import TestCase

from courses.models import Course
from users.models import CustomUser


class CourseModelTest(TestCase):
    author: CustomUser
    course: Course

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = CustomUser.objects.create(
            username='test@test.ru',
            password='testpassword123',
            first_name='Тестовый',
            last_name='Юзер',
            role='teacher'
        )
        cls.course = Course.objects.create(
            author=cls.author,
            title='Тестовый курс',
            description='Тестовое описание',
            price=1000,
            is_active=True
        )

    def test_course_create(self):
        """Тест корректного создания объекта Course."""
        self.assertEqual(self.course.author.__str__(), 'Тестовый Юзер')
        self.assertEqual(self.course.title, 'Тестовый курс')
        self.assertEqual(self.course.description, 'Тестовое описание')
        self.assertEqual(self.course.price, 1000)
        self.assertTrue(self.course.is_active)

    def test_course_str_method(self):
        """Тест метода __str__ модели Course."""
        self.assertEqual(str(self.course), 'Тестовый курс')

    def test_course_price_positive(self):
        """Тест поле price принимает только положительные значения."""
        with self.assertRaises(ValidationError):
            course = Course(
                author=self.author,
                title='Тестовый курс',
                description='Тестовое описаниe',
                price=-1,
                is_active=True
            )
            course.full_clean()

    def test_course_default_ordering(self):
        """Тест сортировки курсов по умолчанию."""
        course_2 = Course.objects.create(
            author=self.author,
            title='Тестовый курс',
            description='Тестовое описание',
            price=1000,
            is_active=True
        )

        courses = Course.objects.all()
        self.assertEqual(courses.first(), course_2)
        self.assertEqual(courses.last(), self.course)
