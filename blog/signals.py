from django.db.models.signals import post_save, pre_save
from django.core.signals import request_started, request_finished
from django.dispatch import receiver
from .models import Post
import threading
import time

# # Thread-local storage for tracking changes
# _thread_locals = threading.local()

# @receiver(post_save, sender=Post)
# def create_post(sender, instance: object, created: bool, **kwargs):
#     if created:
#         print(f"✅ New post created: {instance.title}")
#         print("test")
#         print(kwargs.get('using'))
#         return True

# @receiver(pre_save, sender=Post)
# def track_post_changes(sender, instance, **kwargs):
#     """Track what fields are being changed before saving"""
#     if instance.pk:  # Only for updates, not new instances
#         try:
#             old_instance = Post.objects.get(pk=instance.pk)
#             changed_fields = []
            
#             # Check each field for changes
#             for field in instance._meta.fields:
#                 field_name = field.name
#                 old_value = getattr(old_instance, field_name)
#                 new_value = getattr(instance, field_name)
                
#                 if old_value != new_value:
#                     changed_fields.append({
#                         'field': field_name,
#                         'old_value': old_value,
#                         'new_value': new_value
#                     })
            
#             # Store changes in thread-local storage
#             if not hasattr(_thread_locals, 'post_changes'):
#                 _thread_locals.post_changes = []
#             _thread_locals.post_changes.append({
#                 'post_id': instance.pk,
#                 'post_title': instance.title,
#                 'changes': changed_fields
#             })
            
#         except Post.DoesNotExist:
#             pass

# @receiver(request_started)
# def log_request_started(sender, **kwargs):
#     _thread_locals.start_time = time.time()
#     _thread_locals.post_changes = []  # Initialize changes list
#     print("=== Request Started ===")
#     print(f"Handler: {sender}")
#     print(f"Handler class: {sender.__class__.__name__}")
    
#     # The kwargs contain useful information
#     environ = kwargs.get('environ', {})
    
#     if environ:
#         print(f"Method: {environ.get('REQUEST_METHOD')}")
#         print(f"Path: {environ.get('PATH_INFO')}")
#         print(f"Remote IP: {environ.get('REMOTE_ADDR')}")
#         print(f"User Agent: {environ.get('HTTP_USER_AGENT', 'Unknown')}")
    
#     print("=======================")

# @receiver(request_finished)
# def log_request_finished(sender, **kwargs):
#     """Log request completion and any model changes that occurred"""
#     duration = 0
#     if hasattr(_thread_locals, 'start_time'):
#         duration = time.time() - _thread_locals.start_time
    
#     print("✅ Request processing completed")
#     print(f"⏱️  Request duration: {duration:.3f} seconds")
    
#     # Check for any Post model changes
#     if hasattr(_thread_locals, 'post_changes') and _thread_locals.post_changes:
#         print("\n📝 Post Model Changes Detected:")
#         for change_info in _thread_locals.post_changes:
#             print(f"  Post ID: {change_info['post_id']} - '{change_info['post_title']}'")
#             for change in change_info['changes']:
#                 print(f"    🔄 {change['field']}: '{change['old_value']}' → '{change['new_value']}'")
#         print()
#     else:
#         print("📝 No Post model changes detected in this request")
    
#     # Clean up thread-local data
#     if hasattr(_thread_locals, 'post_changes'):
#         delattr(_thread_locals, 'post_changes')