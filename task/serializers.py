import datetime
from task.models import Category, Task
from rest_framework import serializers
from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'deadline', 'priority', 'status', 'user']

    def validate_deadline(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value
