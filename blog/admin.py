from django.contrib import admin
from .models import Post,Category,Dore,Students,Ticket,Comment,Book
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


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'is_available', 'stock_quantity', 'price', 'created_date']
    list_filter = ['genre', 'language', 'is_available', 'created_date']
    search_fields = ['title', 'author', 'isbn', 'publisher']
    list_editable = ['is_available', 'stock_quantity', 'price']
    readonly_fields = ['created_date', 'updated_date']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'description')
        }),
        ('Details', {
            'fields': ('genre', 'language', 'publisher', 'publication_date', 'page_count')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'is_available', 'stock_quantity')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Book, BookAdmin)
