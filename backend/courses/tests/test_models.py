from django.core.exceptions import ValidationError

from unittest import TestCase

from courses.models import Course


class CourseModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.course = Course.objects.create(
            author='Тестовый автор',
            title='Тестовый курс',
            description='Тестовое описание',
            price=1000,
            is_active=True
        )

    def test_course_create(self):
        """Тест корректного создания объекта Course."""
        self.assertEqual(self.course.author, 'Тестовый автор')
        self.assertEqual(self.course.title, 'Тестовый курс')
        self.assertEqual(self.course.description, 'Тестовое описание')
        self.assertEqual(self.course.price, 1000)
        self.assertTrue(self.course.is_active)

    def test_course_str_method(self):
        """Тест метода __str__ модели Course."""
        self.assertEqual(str(self.course), 'Тестовый курс')

    def test_course_price_positive(self):
        """Тест, что поле price принимает только положительные значения."""
        with self.assertRaises(ValidationError):
            course = Course(
                author='Тестовый автор',
                title='Тестовый курс',
                description='Тестовое описание',
                price=-1,
                is_active=True
            )
            course.full_clean()
