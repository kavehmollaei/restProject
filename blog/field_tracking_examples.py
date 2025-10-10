"""
Comprehensive examples of using request_finished signal to track field updates
in your Post model and other models
"""

from django.db.models.signals import post_save, pre_save
from django.core.signals import request_started, request_finished
from django.dispatch import receiver
from .models import Post, Comment, Category
import threading
import time
import json

# Thread-local storage for tracking changes
_thread_locals = threading.local()

# ============================================================================
# EXAMPLE 1: Basic Field Change Tracking
# ============================================================================

@receiver(pre_save, sender=Post)
def track_post_field_changes(sender, instance, **kwargs):
    """Track changes to Post model fields"""
    if instance.pk:  # Only for updates, not new instances
        try:
            old_instance = Post.objects.get(pk=instance.pk)
            changed_fields = []
            
            # Check each field for changes
            for field in instance._meta.fields:
                field_name = field.name
                old_value = getattr(old_instance, field_name)
                new_value = getattr(instance, field_name)
                
                if old_value != new_value:
                    changed_fields.append({
                        'field': field_name,
                        'old_value': str(old_value),
                        'new_value': str(new_value)
                    })
            
            # Store changes in thread-local storage
            if changed_fields:
                if not hasattr(_thread_locals, 'post_changes'):
                    _thread_locals.post_changes = []
                _thread_locals.post_changes.append({
                    'post_id': instance.pk,
                    'post_title': instance.title,
                    'changes': changed_fields
                })
                
        except Post.DoesNotExist:
            pass

@receiver(request_finished)
def log_post_changes_on_request_finish(sender, **kwargs):
    """Log Post field changes when request finishes"""
    if hasattr(_thread_locals, 'post_changes') and _thread_locals.post_changes:
        print("\n📝 Post Field Changes Detected:")
        for change_info in _thread_locals.post_changes:
            print(f"  Post ID: {change_info['post_id']} - '{change_info['post_title']}'")
            for change in change_info['changes']:
                print(f"    🔄 {change['field']}: '{change['old_value']}' → '{change['new_value']}'")
        print()

# ============================================================================
# EXAMPLE 2: Track Specific Important Fields Only
# ============================================================================

@receiver(pre_save, sender=Post)
def track_important_fields_only(sender, instance, **kwargs):
    """Track only important fields like title, content, status"""
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
                if not hasattr(_thread_locals, 'important_changes'):
                    _thread_locals.important_changes = []
                _thread_locals.important_changes.append({
                    'model': 'Post',
                    'instance_id': instance.pk,
                    'changes': changes
                })
        except Post.DoesNotExist:
            pass

@receiver(request_finished)
def log_important_changes(sender, **kwargs):
    """Log only important field changes"""
    if hasattr(_thread_locals, 'important_changes') and _thread_locals.important_changes:
        print("\n⭐ Important Field Changes:")
        for change in _thread_locals.important_changes:
            print(f"  {change['model']} ID {change['instance_id']}:")
            for field, values in change['changes'].items():
                print(f"    {field}: '{values['old']}' → '{values['new']}'")
        print()

# ============================================================================
# EXAMPLE 3: Track Changes with Request Context
# ============================================================================

@receiver(request_started)
def initialize_request_tracking(sender, **kwargs):
    """Initialize tracking for the request"""
    _thread_locals.start_time = time.time()
    _thread_locals.request_info = {
        'path': kwargs.get('environ', {}).get('PATH_INFO', ''),
        'method': kwargs.get('environ', {}).get('REQUEST_METHOD', ''),
        'remote_addr': kwargs.get('environ', {}).get('REMOTE_ADDR', ''),
    }
    _thread_locals.all_model_changes = []

@receiver(request_finished)
def log_changes_with_context(sender, **kwargs):
    """Log changes with full request context"""
    duration = 0
    if hasattr(_thread_locals, 'start_time'):
        duration = time.time() - _thread_locals.start_time
    
    print(f"\n📊 Request Summary:")
    print(f"  Path: {_thread_locals.request_info.get('path', 'Unknown')}")
    print(f"  Method: {_thread_locals.request_info.get('method', 'Unknown')}")
    print(f"  Duration: {duration:.3f}s")
    print(f"  Remote IP: {_thread_locals.request_info.get('remote_addr', 'Unknown')}")
    
    if hasattr(_thread_locals, 'all_model_changes') and _thread_locals.all_model_changes:
        print(f"  Model Changes: {len(_thread_locals.all_model_changes)}")
        for change in _thread_locals.all_model_changes:
            print(f"    {change}")
    else:
        print("  Model Changes: None")
    print()

# ============================================================================
# EXAMPLE 4: Track Changes with Performance Metrics
# ============================================================================

@receiver(request_finished)
def track_performance_with_changes(sender, **kwargs):
    """Track performance metrics along with field changes"""
    if hasattr(_thread_locals, 'start_time'):
        duration = time.time() - _thread_locals.start_time
        
        change_count = 0
        if hasattr(_thread_locals, 'post_changes'):
            change_count += len(_thread_locals.post_changes)
        if hasattr(_thread_locals, 'important_changes'):
            change_count += len(_thread_locals.important_changes)
        
        print(f"📈 Performance Metrics:")
        print(f"  Request Duration: {duration:.3f}s")
        print(f"  Total Model Changes: {change_count}")
        if duration > 0:
            print(f"  Changes per Second: {change_count/duration:.2f}")
        
        # Log slow requests with changes
        if duration > 1.0 and change_count > 0:
            print(f"⚠️  Slow request detected: {duration:.3f}s with {change_count} changes")

# ============================================================================
# EXAMPLE 5: Track Changes for Multiple Models
# ============================================================================

@receiver(pre_save, sender=Comment)
def track_comment_changes(sender, instance, **kwargs):
    """Track changes to Comment model"""
    if instance.pk:  # Only for updates
        try:
            old_instance = Comment.objects.get(pk=instance.pk)
            changed_fields = []
            
            for field in instance._meta.fields:
                field_name = field.name
                old_value = getattr(old_instance, field_name)
                new_value = getattr(instance, field_name)
                
                if old_value != new_value:
                    changed_fields.append({
                        'field': field_name,
                        'old_value': str(old_value),
                        'new_value': str(new_value)
                    })
            
            if changed_fields:
                if not hasattr(_thread_locals, 'comment_changes'):
                    _thread_locals.comment_changes = []
                _thread_locals.comment_changes.append({
                    'comment_id': instance.pk,
                    'post_id': instance.post.pk,
                    'changes': changed_fields
                })
        except Comment.DoesNotExist:
            pass

@receiver(request_finished)
def log_all_model_changes(sender, **kwargs):
    """Log changes for all models"""
    total_changes = 0
    
    if hasattr(_thread_locals, 'post_changes') and _thread_locals.post_changes:
        print(f"\n📝 Post Changes: {len(_thread_locals.post_changes)}")
        total_changes += len(_thread_locals.post_changes)
    
    if hasattr(_thread_locals, 'comment_changes') and _thread_locals.comment_changes:
        print(f"\n💬 Comment Changes: {len(_thread_locals.comment_changes)}")
        total_changes += len(_thread_locals.comment_changes)
    
    if hasattr(_thread_locals, 'important_changes') and _thread_locals.important_changes:
        print(f"\n⭐ Important Changes: {len(_thread_locals.important_changes)}")
        total_changes += len(_thread_locals.important_changes)
    
    print(f"\n📊 Total Model Changes: {total_changes}")

# ============================================================================
# EXAMPLE 6: Export Changes as JSON
# ============================================================================

@receiver(request_finished)
def export_changes_as_json(sender, **kwargs):
    """Export all changes as JSON for external processing"""
    changes_data = {
        'timestamp': time.time(),
        'request_info': _thread_locals.request_info if hasattr(_thread_locals, 'request_info') else {},
        'changes': {}
    }
    
    if hasattr(_thread_locals, 'post_changes') and _thread_locals.post_changes:
        changes_data['changes']['posts'] = _thread_locals.post_changes
    
    if hasattr(_thread_locals, 'comment_changes') and _thread_locals.comment_changes:
        changes_data['changes']['comments'] = _thread_locals.comment_changes
    
    if hasattr(_thread_locals, 'important_changes') and _thread_locals.important_changes:
        changes_data['changes']['important'] = _thread_locals.important_changes
    
    # Print JSON (in real app, you might save to file or send to external service)
    if changes_data['changes']:
        print("\n📄 Changes as JSON:")
        print(json.dumps(changes_data, indent=2))

# ============================================================================
# EXAMPLE 7: Cleanup and Memory Management
# ============================================================================

@receiver(request_finished)
def cleanup_tracking_data(sender, **kwargs):
    """Clean up thread-local data to prevent memory leaks"""
    cleanup_attrs = [
        'start_time', 'post_changes', 'comment_changes', 
        'important_changes', 'request_info', 'all_model_changes'
    ]
    
    for attr in cleanup_attrs:
        if hasattr(_thread_locals, attr):
            delattr(_thread_locals, attr)
    
    print("🧹 Tracking data cleaned up")

# ============================================================================
# EXAMPLE 8: Conditional Tracking Based on Request Type
# ============================================================================

@receiver(request_finished)
def conditional_tracking(sender, **kwargs):
    """Only track changes for specific request types"""
    if hasattr(_thread_locals, 'request_info'):
        path = _thread_locals.request_info.get('path', '')
        method = _thread_locals.request_info.get('method', '')
        
        # Only track changes for API requests or admin requests
        if '/api/' in path or '/admin/' in path:
            if hasattr(_thread_locals, 'post_changes') and _thread_locals.post_changes:
                print(f"🔍 API/Admin Changes for {method} {path}:")
                for change in _thread_locals.post_changes:
                    print(f"  Post {change['post_id']}: {len(change['changes'])} fields changed")
        else:
            print("📝 Regular request - minimal change tracking")
