from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, TaskStatusUpdateSerializer
from accounts.models import User
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show projects from the user's organization
        return Project.objects.filter(organization=self.request.user.organization)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, organization=self.request.user.organization)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(organization=self.request.user.organization)

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'assigned_to', 'project']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'status']

    def get_queryset(self):
        user = self.request.user
        org_tasks = Task.objects.filter(project__organization=user.organization)
        
        # Admins and Managers see all tasks in their org
        if user.role in ['ADMIN', 'MANAGER']:
            return org_tasks
        
        # Members only see tasks assigned to them
        return org_tasks.filter(Q(assigned_to=user) | Q(created_by=user))

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        task._current_user = self.request.user  # For audit logging
        task.save()

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        org_tasks = Task.objects.filter(project__organization=user.organization)
        
        if user.role in ['ADMIN', 'MANAGER']:
            return org_tasks
        
        return org_tasks.filter(Q(assigned_to=user) | Q(created_by=user))
        # ADD THESE METHODS
    def perform_update(self, serializer):
        task = serializer.save()
        task._current_user = self.request.user  # For audit logging
        task.save()

    def perform_destroy(self, instance):
        instance._current_user = self.request.user  # For audit logging
        instance.delete()
class TaskStatusUpdateView(generics.UpdateAPIView):
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow updating status of tasks assigned to the user
        return Task.objects.filter(
            project__organization=self.request.user.organization,
            assigned_to=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save()
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer