from django.contrib import admin
from .models import Profile, Post, Comment, ArticlePost, Category

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile_img_tag', 'user', 'city', 'contact')
    search_fields = ('city',)
    list_per_page = 10

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_text', 'content_image', 'content_file', 'date_created')
    list_per_page = 5
    search_fields = ('id',)
    list_filter = ('creator',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)



# For Articles
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_tag','cat_title', 'description', 'url', 'date_added')
    

@admin.register(ArticlePost)
class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', )
    list_per_page = 10
    search_fields = ('title',)
    list_filter = ('category',)
