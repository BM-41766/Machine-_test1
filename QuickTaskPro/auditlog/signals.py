from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tasks.models import Task
from auditlog.models import TaskAuditLog
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Task)
def log_task_changes(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    user = kwargs.get('request_user') if 'request_user' in kwargs else None
    
    if not user and hasattr(instance, '_current_user'):
        user = instance._current_user
    
    if not user:
        return

    changes = {}
    if not created:
        # Compare current values with previous values
        old_instance = Task.objects.get(pk=instance.pk)
        for field in ['title', 'description', 'status', 'due_date', 'assigned_to']:
            old_value = getattr(old_instance, field)
            new_value = getattr(instance, field)
            if old_value != new_value:
                changes[field] = {
                    'old': str(old_value),
                    'new': str(new_value)
                }

    TaskAuditLog.objects.create(
        task=instance,
        action=action,
        changed_by=user,
        changes=changes
    )

@receiver(post_delete, sender=Task)
def log_task_deletion(sender, instance, **kwargs):
    user = kwargs.get('request_user') if 'request_user' in kwargs else None
    
    if not user and hasattr(instance, '_current_user'):
        user = instance._current_user
    
    if not user:
        return

    TaskAuditLog.objects.create(
        task=instance,
        action='DELETE',
        changed_by=user,
        changes={}
    )