from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

from read_statistics.utils import read_statistics_once_read
from.models import BlogType, Blog


def get_blog_common_list(request, blogs_all_list):
    context = {}
    paginator = Paginator(blogs_all_list, 3)
    page_num = request.GET.get('page', 1)  # 获取url里的参数，默认打开第一页1
    blog_dates = Blog.objects.dates('create_time', 'month', order='ASC')
    '''
    Django提供的方法,
    get_page:非法字符统一处理，
    超过或者其他非法字符统一返回1
    '''
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 当前页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num + 1)) + list(
        range(current_page_num + 1, min(current_page_num + 3, paginator.num_pages + 1)))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = blog_dates
    return context


def index(request):  # 首页
    blogs = Blog.objects.all()[:5]
    return render(request, 'blog/index.html', {'blogs': blogs})


def blog_list(request):  # 博客列表
    blogs_all_list = Blog.objects.all()
    context = get_blog_common_list(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):  # 博客详情
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)  # 可能请求主键值没有对应的博客那么就返回404
    read_cookie_key = read_statistics_once_read(request, blog)
    context['blog'] = blog
    context['pre_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    '''
    筛选博客创建时间大于当前博客创建时间的博客里的最后一条
    '''
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response


def blogs_with_type(request, blog_type_pk):  # 博客分类
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_common_list(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blog_with_date(request, year, month):  # 博客归档
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = get_blog_common_list(request, blogs_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_type.html', context)


def search(request):  # 搜索
    context = {}
    kew_word = request.GET.get('search')
    try:
        search_blogs = Blog.objects.filter(Q(content__contains=kew_word) | Q(title__contains=kew_word))
    except Exception:
        return HttpResponse('未查询到相关博客')
    number = search_blogs.count()
    context['kew_word'] = kew_word
    context['search_blogs'] = search_blogs
    context['number'] = number
    return render(request, 'blog/blog_search.html', context)
