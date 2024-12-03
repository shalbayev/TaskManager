import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from task.models import Task, Category

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(username="testuser", password="password"):
        return User.objects.create_user(username=username, password=password)

    return make_user


@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def create_category(db):
    def make_category(name="Work", description="Work-related tasks"):
        return Category.objects.create(name=name, description=description)

    return make_category


@pytest.fixture
def create_task(db, create_user, create_category):
    def make_task(user=None, category=None, title="Test Task"):
        if user is None:
            user = create_user()
        if category is None:
            category = create_category()
        return Task.objects.create(
            title=title,
            description="Test Description",
            category=category,
            deadline="2024-12-01",
            priority="M",
            status="TO DO",
            user=user
        )

    return make_task


@pytest.mark.django_db
def test_create_task(auth_client, create_category):
    client, user = auth_client
    category = create_category()
    payload = {
        "title": "New Task",
        "description": "Description of the task",
        "category": category.id,
        "deadline": "2024-12-31",
        "priority": "M",
        "status": "TO DO"
    }

    response = client.post('/api/taskman/tasks/', payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    assert Task.objects.first().title == "New Task"
    assert Task.objects.first().user == user


@pytest.mark.django_db
def test_get_tasks(auth_client, create_task):
    client, user = auth_client
    task = create_task(user=user)

    response = client.get('/api/taskman/tasks/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == task.title


@pytest.mark.django_db
def test_update_task(auth_client, create_task):
    client, user = auth_client
    task = create_task(user=user)

    payload = {
        "title": "Updated Task",
        "description": "Updated description",
        "category": task.category.id,
        "deadline": "2024-12-31",
        "priority": "H",
        "status": "IN PROGRESS"
    }

    response = client.put(f'/api/taskman/tasks/{task.id}/', payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == "Updated Task"
    assert task.priority == "H"


@pytest.mark.django_db
def test_delete_task(auth_client, create_task):
    client, user = auth_client
    task = create_task(user=user)

    response = client.delete(f'/api/taskman/tasks/{task.id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_filter_tasks_by_category(auth_client, create_task, create_category):
    client, user = auth_client
    category = create_category(name="Personal")
    create_task(user=user, category=category, title="Personal Task")

    response = client.get(f'/api/taskman/tasks/by_category/?category={category.id}')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Personal Task"
