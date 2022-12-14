
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# custom manager class to get published posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')


# for Posting, all the things required
class Post(models.Model):
    # used later for blog status
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    # The title of the blog
    title = models.CharField(max_length=250)
    # slug is for SEO-friendly URLs
    # Django will prevent multiple posts from having the same slug for a given date
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # Defines a many-to-one relationship (One user can have many blogs)
    # on_delete specifies the behaviour to adopt when the referenced object is deleted (in this case the author)
    # CASCADE is an SQL feature which will delete all related blogs when the author is deleted
    # define the reverse relationship using the related_name
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    # DateTimeField indicates when the post is published
    publish = models.DateTimeField(default=timezone.now)
    # auto_new_add saves the date automatically
    created = models.DateTimeField(auto_now_add=True)
    # almost the same thing as automatically saving the date
    updated = models.DateTimeField(auto_now=True)
    # this variable can only have 2 options 'draft' and 'published'
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager
    # tags have a many-to-many relationship to posts
    tags = TaggableManager() # Taggagle Manager allows the addition/removal/retreival of tags
    # descending order using the negative prefix, posts published recently will appear first
    class Meta:
        ordering = ('-publish',)

    # returns the human-readable representation of the object
    def __str__(self):
        return self.title

    # Canonical url for post_detail
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])

class Comment(models.Model):
    # Post is a database object with a one to many relationship with comments
    # One Post can have many comments
    # Comments on a post can be accessed by Post.comments.all() because of the 'comments' related_name
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # for disabling inappropriate comments
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'

