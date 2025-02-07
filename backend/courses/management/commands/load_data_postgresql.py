import getpass

from django.core.management.base import BaseCommand
from django.db import connection

from courses.models import Course, Group, Lesson
from users.models import CustomUser, Purchase


class Command(BaseCommand):
    help = 'Очищает базу, сбрасывает ID и создает тестовые данные'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('-- Начинаем процесс сброса базы --'))

        # 1. Очистка базы
        self.stdout.write(self.style.WARNING('-- Удаляем все данные --'))
        Purchase.objects.all().delete()
        Group.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        CustomUser.objects.all().delete()

        # 2. Сброс ID (если база - SQLite)
        self.reset_sequences(
            ['users_customuser', 'courses_course', 'courses_lesson', 'courses_group', 'users_purchase']
        )

        self.stdout.write(self.style.SUCCESS('-- База очищена и ID сброшены --'))

        # 3. Создание тестовых данных
        self.create_test_data()

        self.stdout.write(self.style.SUCCESS('-- Данные успешно загружены! --'))

    def reset_sequences(self, tables):
        """Сбрасывает автоинкрементные ID в PostgreSQL."""
        with connection.cursor() as cursor:
            for table in tables:
                cursor.execute(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1;")

    def create_test_data(self):
        """Создает тестовые данные."""
        self.stdout.write(self.style.WARNING('-- Создаем тестовых пользователей --'))

        password = getpass.getpass('Введите пароль для всех тестовых пользоватлей: ')

        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@admin.ru',
            first_name='Админ',
            last_name='Тест',
            role='admin'
        )
        admin.set_password(password)
        admin.save()

        teacher = CustomUser.objects.create_user(
            username='teacher',
            email='teacher@teacher.ru',
            first_name='Преподаватель',
            last_name='Тест',
            role='teacher'
        )
        teacher.set_password(password)
        teacher.save()

        student = CustomUser.objects.create_user(
            username='student',
            email='student@student.ru',
            first_name='Студент',
            last_name='Тест',
            role='student'
        )
        student.set_password(password)
        student.save()

        print('\n\tЛогины тестовых пользователей:',
              f'Админ - {admin.email}',
              f'Преподаватель - {teacher.email}',
              f'Студент - {student.email}\n', sep='\n\t')

        self.stdout.write(self.style.SUCCESS('-- Пользователи созданы --'))

        self.stdout.write(self.style.WARNING('-- Создаем тестовые курсы и уроки --'))
        course = Course.objects.create(
            author=teacher,
            title='Курс по Django',
            description='Изучение Django с нуля',
            price=100,
            is_active=True
        )

        lesson = Lesson.objects.create(
            course=course,
            title='Введение в Django',
            link='http://127.0.0.1:8000/api/v1/courses/1/lessons/1/'
        )

        self.stdout.write(self.style.SUCCESS('-- Курсы и уроки созданы --'))
