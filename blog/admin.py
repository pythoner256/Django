from django.contrib import admin
from blog.models import Blog, BlogType


class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'get_read_num', 'blog_type', 'author', 'create_time', 'last_updated_time']


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogType, BlogTypeAdmin)

