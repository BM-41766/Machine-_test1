from rest_framework import serializers
from .models import Project, Task
from accounts.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'organization', 'created_by', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 
                  'project', 'assigned_to', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']