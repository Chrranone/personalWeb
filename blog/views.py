from django.shortcuts import get_object_or_404,render
from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import read_statistics_once_read
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm


def get_blog_list_commom_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)  #每10进行分页
    page_num = request.GET.get('page',1)  #获取页码参数get请求
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number #获取当前页码
    #获取当前页码前后两页的范围
    page_range = list(range(max(currentr_page_num-2,1),currentr_page_num)) +\
                list(range(currentr_page_num,min(currentr_page_num+2,paginator.num_pages)+1))
    
    #加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取博客分类对应的博客数量
    BlogType.objects.annotate(blog_count=Count('blog'))
    '''blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    '''
    
    #获取日期归档 对应博客数量
    blog_dates = Blog.objects.dates('created_time','month',order="DESC")
    '''blog_dates = Blog.objects.dates('created_time','month',order="DESC")\
                    .annotate(blog_count)=Count('created_time')
    blog_dates_dict = {}
    for blog_date in blog_dates[::2]:
    '''
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year).count
        blog_dates_dict[blog_date] = blog_count
    

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    #context['blog_types'] = blog_types_list
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_commom_data(request,blogs_all_list)
    return render(request,'blog/blog_list.html',context)

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_commom_data(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request,'blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year)
    context = get_blog_list_commom_data(request,blogs_all_list)
    context['blogs_with_date'] = '%s年' % (year)
    return render(request,'blog/blogs_with_date.html',context)
   
def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)
    #blog_content_type = ContentType.objects.get_for_model(blog)
    #comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)

    context = {}
    context['blog'] = blog
    #context['user'] = request.user
    #context['comments'] = comments.order_by('-comment_time')
    #context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk,'reply_comment_id':0})
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render(request,'blog/blog_detail.html',context)  #响应
    response.set_cookie(read_cookie_key,'true')  #阅读cookie标记
    return response