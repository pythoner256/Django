from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm


def update_comment(request):  # 提交评论内容保存到后台
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        # 返回数据
        data = {}
        data['status'] = "SUCCESS"
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')  # 转换时间格式
        data['text'] = comment.text

        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
        return JsonResponse(data)
    else:
        # return render(request, 'blog/error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data = {}
        data['status'] = "ERROR"
        data['message'] = list(comment_form.errors.values())[0][0]
        return JsonResponse(data)