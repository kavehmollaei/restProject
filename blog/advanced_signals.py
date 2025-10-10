"""
Advanced examples of using request_finished signal to track model field updates
"""
from django.db.models.signals import post_save, pre_save
from django.core.signals import request_started, request_finished
from django.dispatch import receiver
from .models import Post, Comment
import threading
import time
import json
from django.db import transaction

# Thread-local storage for tracking changes
_thread_locals = threading.local()

# Example 1: Track specific field changes
@receiver(pre_save, sender=Post)
def track_specific_fields(sender, instance, **kwargs):
    """Track changes to specific important fields"""
    if instance.pk:  # Only for updates
        try:
            old_instance = Post.objects.get(pk=instance.pk)
            important_fields = ['title', 'content', 'status', 'category']
            changes = {}
            
            for field in important_fields:
                old_value = getattr(old_instance, field)
                new_value = getattr(instance, field)
                
                if old_value != new_value:
                    changes[field] = {
                        'old': str(old_value),
                        'new': str(new_value)
                    }
            
            if changes:
                if not hasattr(_thread_locals, 'field_changes'):
                    _thread_locals.field_changes = []
                _thread_locals.field_changes.append({
                    'model': 'Post',
                    'instance_id': instance.pk,
                    'changes': changes
                })
        except Post.DoesNotExist:
            pass

# Example 2: Track all model changes with detailed logging
@receiver(request_started)
def initialize_change_tracking(sender, **kwargs):
    """Initialize tracking for the request"""
    _thread_locals.start_time = time.time()
    _thread_locals.all_changes = []
    _thread_locals.field_changes = []
    print("🔍 Change tracking initialized")

@receiver(request_finished)
def log_all_changes(sender, **kwargs):
    """Log all model changes that occurred during the request"""
    duration = 0
    if hasattr(_thread_locals, 'start_time'):
        duration = time.time() - _thread_locals.start_time
    
    print(f"\n📊 Request Summary (Duration: {duration:.3f}s)")
    print("=" * 50)
    
    # Log field-specific changes
    if hasattr(_thread_locals, 'field_changes') and _thread_locals.field_changes:
        print("🔄 Field Changes Detected:")
        for change in _thread_locals.field_changes:
            print(f"  Model: {change['model']} (ID: {change['instance_id']})")
            for field, values in change['changes'].items():
                print(f"    {field}: '{values['old']}' → '{values['new']}'")
        print()
    
    # Log all changes
    if hasattr(_thread_locals, 'all_changes') and _thread_locals.all_changes:
        print("📝 All Model Changes:")
        for change in _thread_locals.all_changes:
            print(f"  {change}")
        print()
    
    if not (hasattr(_thread_locals, 'field_changes') and _thread_locals.field_changes) and \
       not (hasattr(_thread_locals, 'all_changes') and _thread_locals.all_changes):
        print("📝 No model changes detected")
    
    print("=" * 50)

# Example 3: Track changes with database logging
class ModelChangeLog(models.Model):
    model_name = models.CharField(max_length=100)
    instance_id = models.PositiveIntegerField()
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    request_path = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-timestamp']

@receiver(request_finished)
def save_changes_to_database(sender, **kwargs):
    """Save model changes to database for audit trail"""
    if hasattr(_thread_locals, 'field_changes') and _thread_locals.field_changes:
        environ = kwargs.get('environ', {})
        request_path = environ.get('PATH_INFO', '')
        
        for change in _thread_locals.field_changes:
            for field, values in change['changes'].items():
                ModelChangeLog.objects.create(
                    model_name=change['model'],
                    instance_id=change['instance_id'],
                    field_name=field,
                    old_value=values['old'],
                    new_value=values['new'],
                    request_path=request_path
                )
        print("💾 Changes saved to database")

# Example 4: Track changes with JSON export
@receiver(request_finished)
def export_changes_json(sender, **kwargs):
    """Export changes as JSON for external processing"""
    if hasattr(_thread_locals, 'field_changes') and _thread_locals.field_changes:
        changes_data = {
            'timestamp': time.time(),
            'request_info': {
                'path': kwargs.get('environ', {}).get('PATH_INFO', ''),
                'method': kwargs.get('environ', {}).get('REQUEST_METHOD', ''),
            },
            'changes': _thread_locals.field_changes
        }
        
        # You could save this to a file or send to external service
        print("📄 Changes exported as JSON:")
        print(json.dumps(changes_data, indent=2))

# Example 5: Track changes with performance metrics
@receiver(request_finished)
def track_performance_metrics(sender, **kwargs):
    """Track performance metrics related to model changes"""
    if hasattr(_thread_locals, 'start_time'):
        duration = time.time() - _thread_locals.start_time
        
        change_count = 0
        if hasattr(_thread_locals, 'field_changes'):
            change_count = len(_thread_locals.field_changes)
        
        print(f"📈 Performance Metrics:")
        print(f"  Request Duration: {duration:.3f}s")
        print(f"  Model Changes: {change_count}")
        print(f"  Changes per Second: {change_count/duration if duration > 0 else 0:.2f}")

# Example 6: Conditional change tracking based on request type
@receiver(request_finished)
def conditional_change_tracking(sender, **kwargs):
    """Only track changes for specific request types"""
    environ = kwargs.get('environ', {})
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', '')
    
    # Only track changes for API requests or admin requests
    if '/api/' in path or '/admin/' in path:
        if hasattr(_thread_locals, 'field_changes') and _thread_locals.field_changes:
            print(f"🔍 API/Admin Changes for {method} {path}:")
            for change in _thread_locals.field_changes:
                print(f"  {change['model']} ID {change['instance_id']}: {len(change['changes'])} fields changed")
    else:
        print("📝 Regular request - no detailed change tracking")

# Example 7: Track changes with user context
@receiver(request_finished)
def track_changes_with_user_context(sender, **kwargs):
    """Track changes with user information"""
    if hasattr(_thread_locals, 'field_changes') and _thread_locals.field_changes:
        # You could get user from request if available
        print("👤 User Context Changes:")
        for change in _thread_locals.field_changes:
            print(f"  User made changes to {change['model']} ID {change['instance_id']}")
            for field, values in change['changes'].items():
                print(f"    Modified {field}: '{values['old']}' → '{values['new']}'")

# Example 8: Cleanup and memory management
@receiver(request_finished)
def cleanup_change_tracking(sender, **kwargs):
    """Clean up thread-local data to prevent memory leaks"""
    cleanup_attrs = ['start_time', 'field_changes', 'all_changes', 'post_changes']
    for attr in cleanup_attrs:
        if hasattr(_thread_locals, attr):
            delattr(_thread_locals, attr)
    print("🧹 Change tracking data cleaned up")

