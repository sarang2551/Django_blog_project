from typing import List
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status="published")
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        sent_mail = False
        if form.is_valid():
            # Form field passes validation
            cd = form.cleaned_data() # dictionary object with valid data from a user (not necessarily the author)
            #....send email
            post_url = request.build_absolute_url(post.get_absolute_url()) # getting the post detail url
            email_subject = f'{cd.name} recommends you read {post.title}'
    else:
        # if the method is 'GET' then display an empty form
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post,'form':form})
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# request parameter is required by all views
def post_list(request):
    posts = Post.published.all()
    pagi = Paginator(posts,3) # 3 pages in each page
    page = request.GET.get('page') # indicates the page number (page is an integer)
    try:
        p = pagi.page(page) # return the page number specified
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        p = pagi.page(1)
    except EmptyPage:
        # if page is out of index deliver the last page
        p = pagi.page(pagi.num_pages)
    return render(request, 'blog/post/list.html', {'page':page , 'posts': p})


# retrieve one post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    return render(request, 'blog/post/detail.html', {'post': post})
