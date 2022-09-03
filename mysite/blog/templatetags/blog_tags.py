from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
# register a tag called "total_posts"
@register.simple_tag(name='total_posts')
def total_posts():
    return Post.published.count()

# inclusion tags allow the rendering of context variables into a template
# the path to the template file in passed as an arguement 
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    # slice the list of posts to only show the top 5
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

# a reusable variable that returns blogs with the most comments
@register.simple_tag
def get_most_commented_posts(count = 5):
    # annonate to aggregate the total number of comments
    # slice to show the top count posts
    return Post.published.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]

# mark_safe so Django doesn't skip the HTML code from the markdown
# {{variable|markdown}}
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))