from typing import List
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

# django workflow
# python component --> view --> registering url --> template

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status="published")
    sent_mail = False
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field passes validation
            cd = form.cleaned_data() # dictionary object with valid data from a user (not necessarily the author)
            #....send email
            post_url = request.build_absolute_url(post.get_absolute_url()) # getting the post detail url
            email_subject = f'{cd.name} recommends you read {post.title} at {post_url}'
            email_message = f'Read {post.title} at {post.url}\n\n {cd.name}\'s comments {cd.comments}.'
            send_mail(email_subject,email_message,'sarang.nirwan@gmail.com',cd.to)
            sent_mail = True
    else:
        # if the method is 'GET' then display an empty form
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post,'form':form,'sent':sent_mail})
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# request parameter is required by all views
def post_list(request, tag_slug = None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
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
    return render(request, 'blog/post/list.html', {'page':page , 'posts': p,'tag':tag})


# retrieve one post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    # retrive all comments associated to the post, filtering them to only get active comments
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        # Post request for a comment
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create a comment object, a Comment object is automatically formed from the save method as a Model is linked to the CommentForm class
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        # if the request is GET then display an empty form
        comment_form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id',flat=True)
    # Get all posts that contain any of the tags in the current post excluding the current post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Order the similar posts based on shared tags and published date, slice the result to obtain the first 4 
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post,
    'comments':comments,
    'new_comment':new_comment,
    'comment_form':comment_form,
    'similar_posts':similar_posts,
    })
