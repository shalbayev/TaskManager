from django.db import models

from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    deadline = models.DateField()
    PRIO_CHOICES = (
        ('L', 'Низкий'),
        ('M', 'Средний'),
        ('H', 'Высокий')
    )
    priority = models.CharField(max_length=100, choices=PRIO_CHOICES)
    STATUS_CHOICES = (
        ('TO DO', 'Надо сделать'),
        ('IN PROGRESS', 'В процессе'),
        ('DONE', 'Сделано'),
        ('ON HOLD', 'Приостановлено')
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
