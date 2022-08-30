from django.contrib import admin
from .models import Post


# add this model to the admin site for easy interfacing
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # the list_display attribute allows to set the fields of the model that I want to display
    list_display = ("title", "slug", "author", "publish", "status")
    # filtering options for the table
    list_filter = ('status', 'created', 'publish', 'author')

    search_fields = ('title', 'body')

    prepopulated_fields = {'slug': ('title',)}
    # better than a drop-down widget when you have thousands of users
    raw_id_fields = ('author',)

    date_hierarchy = 'publish'
    # default ordering attribute
    ordering = ('status', 'publish')
# Register your models here.
