from django.contrib import admin
from .models import Post,Category,Dore,Students,Ticket,Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display= ['auther','title','category','status','updated_date','published_date']


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Dore)
admin.site.register(Students)
admin.site.register(Ticket)

class TicketAdmin(admin.ModelAdmin):
    list_display=['name','post','phone']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','name','created','active']
    list_editable = ['active']
    list_filter = ['active']
    search_fields = ['name','body']
