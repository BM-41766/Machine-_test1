from django.db import models
from tasks.models import Task
from accounts.models import User

class TaskAuditLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    )
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField()  # Stores field changes

    def __str__(self):
        return f"{self.task} - {self.action} by {self.changed_by}"