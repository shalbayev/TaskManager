from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task.views import TaskViewSet, CategoryViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]