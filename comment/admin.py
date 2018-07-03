from django.contrib import admin
from.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'text', 'comment_time', 'user']


admin.site.register(Comment, CommentAdmin)



