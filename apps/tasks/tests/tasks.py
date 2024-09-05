from datetime import timedelta
from enum import unique
from unittest import TestCase

from django.utils import timezone
from apps.projects.models import Project
from apps.tasks.choices.priorities import Priority
from apps.tasks.models import Tag, Task
from apps.tasks.serializers.task_serializers import CreateUpdateTaskSerializer, TaskDetailSerializer
from apps.users.models import User
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agile.settings')

class CreateTaskTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
                name='Test Project',
                description="Test description for the test project name for the Unit tests."
        )
        self.tag1 = Tag.objects.create(id=1, name='Backend')
        self.tag2 = Tag.objects.create(id=2, name='DevOPS')
        self.user = User.objects.create(
            username='test_user',
            first_name='test',
            last_name='uer',
            email='user@example.com',
            position="PRODUCT_OWNER",
            password='1q9i2w8u3e7y4r6t5'
        )


    def test_valid_task_data(self):
        valid_data = dict(name='Valid Task Name',
                          description='This is a valid task description with more than 50 characters.',
                          priority=Priority.HIGH[0], project=self.project.name, tags=[1, 2],
                          deadline=timezone.now() + timedelta(days=10))
        serializer = CreateUpdateTaskSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIsInstance(serializer.validated_data['name'], str)
        self.assertIsInstance(serializer.validated_data['description'],str)
        self.assertIsInstance(serializer.validated_data['priority'], int)
        self.assertIsInstance(serializer.validated_data['project'], Project)
        self.assertIsInstance(serializer.validated_data['tags'], list)

        for tag in serializer.validated_data['tags']:
            self.assertIsInstance(tag, Tag)
            self.assertIsInstance(serializer.validated_data['deadline'], timezone.datetime)


    def test_short_name(self):
        invalid_data = dict(name='Short', description='This is a valid task description with more than 50 characters.',
                            priority=Priority.HIGH[0], project=self.project.name, tags=[1, 2],
                            deadline=timezone.now() + timedelta(days=10))
        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertEqual(serializer.errors['name'][0], 'Name must be at least 10 characters')

    def test_short_description(self):
        invalid_data = dict(name='Valid Task Name', description='Short description.', priority=Priority.HIGH[0],
                            project=self.project.name, tags=[1, 2], deadline=timezone.now() + timedelta(days=10))
        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertEqual(serializer.errors['description'][0], 'Description must be at least 50 characters')



class TaskDetailTestCase(TestCase):
    def unique_name():
        counter = 1
        while True:
            name = f'TestProject{counter}'
            if not Project.objects.filter(name=name).exists():
                return name
            counter += 1

    def unique_email():
        counter = 1
        while True:
            email = f'testuser{counter}@example.com'
            if not User.objects.filter(email=email).exists():
                return email
            counter += 1

    def setUp(self):
        Project.objects.all().delete()
        self.project = Project.objects.create(name=self.unique_name())
        self.tag1 = Tag.objects.create(name='Backend')
        self.tag2 = Tag.objects.create(name='DevOPS')
        self.user = User.objects.create(
            username='test_user',
            first_name='test',
            last_name='uer',
            email=self.unique_email(),
            position="PRODUCT_OWNER",
            password='1q9i2w8u3e7y4r6t5'
        )
        self.task = Task.objects.create(
            name='Valid Task Name',
            description='This is a valid task description with more than 50 characters.',
            priority=Priority.HIGH[0],
            project=self.project,
            deadline=timezone.now() + timedelta(days=10),
            assignee=self.user
        )
        self.task.tags.add(self.tag1, self.tag2)

    def test_task_detail_serializer_tags(self):
        serializer = TaskDetailSerializer(instance=self.task)
        data = serializer.data

        # Проверка, что теги возвращаются корректно
        tags = [{'id': tag.id, 'name': tag.name} for tag in self.task.tags.all()]
        self.assertEqual(data['tags'], tags)

        # Проверка типов данных для тегов
        self.assertIsInstance(data['tags'], list)
        self.assertTrue(all(isinstance(tag, dict) for tag in data['tags']))