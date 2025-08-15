from django.urls import path
from .views import (
    ProjectListCreateView, ProjectDetailView,
    TaskListCreateView, TaskDetailView, TaskStatusUpdateView
)

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task-status-update'),
]