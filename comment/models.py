from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING)

    root = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING, related_name='root_comment')
    ''''
    记录顶级评论，方便在前端页面展示（顶级评论下的所有回复）
    '''
    parent = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING, related_name='parent_comment')
    '''
    记录上一级评论对象的主键值
    '''
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.DO_NOTHING)  # 回复谁

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
