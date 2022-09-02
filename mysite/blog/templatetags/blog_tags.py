from django import template
from ..models import Post

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