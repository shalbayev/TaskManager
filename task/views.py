from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_done(self, request, pk=None):
        task = self.get_object()
        task.status = 'DONE'
        task.save()
        return Response({'status': 'Task marked as done'})

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        print(query)
        category = request.query_params.get('category', '')
        print(category)
        status = request.query_params.get('status', '')
        print(status)
        queryset = Task.objects.filter(user=request.user)
        print(queryset)

        if query:
            queryset = queryset.filter(title__icontains=query)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if status:
            queryset = queryset.filter(status=status)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category', None)
        if category_id:
            tasks = Task.objects.filter(user=request.user, category_id=category_id)
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category ID is required'}, status=400)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]