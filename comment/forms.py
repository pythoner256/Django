from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor .widgets import CKEditorWidget
from . models import Comment


class CommentForm(forms.Form):
    text = forms.CharField(widget=CKEditorWidget(config_name='comment-ckeditor'),
                           error_messages={'required': '评论内容不能为空'})
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))  # 设置回复对应评论的id值

    '''将user传入并进行验证'''
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):  # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise ValueError('用户未登录')
        '''
        判断评论对象是否存在
        '''
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise ValueError('评论对象不存在')
        return self.cleaned_data

    def clean_reply_comment_id(self):  # 验证回复
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        if reply_comment_id == 0:  # 是顶级评论就将parent设置为None
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():  # 判断主键值在数据库中是否存在
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id
