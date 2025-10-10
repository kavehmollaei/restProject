"""
Simple example showing how to use request_finished signal to track field updates
in your Post model. This is a minimal, working example.
"""

from django.db.models.signals import pre_save
from django.core.signals import request_started, request_finished
from django.dispatch import receiver
from blog.models import Post
import threading
import time

# Thread-local storage
_thread_locals = threading.local()

@receiver(request_started)
def start_tracking(sender, **kwargs):
    """Initialize tracking when request starts"""
    _thread_locals.start_time = time.time()
    _thread_locals.changes = []
    print("🔍 Field change tracking started")

@receiver(pre_save, sender=Post)
def track_post_updates(sender, instance, **kwargs):
    """Track what fields are being updated in Post model"""
    if instance.pk:  # Only for updates, not new posts
        try:
            old_post = Post.objects.get(pk=instance.pk)
            changes = []
            
            # Check each field for changes
            for field in instance._meta.fields:
                field_name = field.name
                old_value = getattr(old_post, field_name)
                new_value = getattr(instance, field_name)
                
                if old_value != new_value:
                    changes.append({
                        'field': field_name,
                        'old': str(old_value),
                        'new': str(new_value)
                    })
            
            # Store changes if any
            if changes:
                _thread_locals.changes.append({
                    'post_id': instance.pk,
                    'post_title': instance.title,
                    'changes': changes
                })
                
        except Post.DoesNotExist:
            pass

@receiver(request_finished)
def show_updated_fields(sender, **kwargs):
    """Show which fields were updated when request finishes"""
    duration = 0
    if hasattr(_thread_locals, 'start_time'):
        duration = time.time() - _thread_locals.start_time
    
    print(f"\n✅ Request completed in {duration:.3f} seconds")
    
    if hasattr(_thread_locals, 'changes') and _thread_locals.changes:
        print("\n📝 Updated Fields in Post Model:")
        for change_info in _thread_locals.changes:
            print(f"  Post ID {change_info['post_id']}: '{change_info['post_title']}'")
            for change in change_info['changes']:
                print(f"    🔄 {change['field']}: '{change['old']}' → '{change['new']}'")
        print()
    else:
        print("📝 No Post fields were updated in this request")
    
    # Clean up
    if hasattr(_thread_locals, 'changes'):
        delattr(_thread_locals, 'changes')

# Example usage:
"""
To use this in your Django project:

1. Make sure this code is in your signals.py file
2. Import it in your apps.py ready() method
3. When you update a Post model, you'll see output like:

🔍 Field change tracking started
✅ Request completed in 0.045 seconds

📝 Updated Fields in Post Model:
  Post ID 1: 'My Post Title'
    🔄 title: 'Old Title' → 'New Title'
    🔄 content: 'Old content' → 'New content'
    🔄 status: 'False' → 'True'

This shows exactly which fields were changed and their old/new values.
"""

