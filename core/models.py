from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.html import format_html
from tinymce.models import HTMLField

User = get_user_model()

# Create your models here.

#Model for profile
def default_profile_pic_path(instance, filename):
    # Generate the file path for the default profile picture
    return 'profile_pics/def-user.jpg'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=default_profile_pic_path, default='def-user.jpg')
    bio = models.TextField(max_length=500, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50, blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True,)
    followings = models.ManyToManyField(User, related_name='followings', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_post_count(self):
        return self.user.post_set.count()
    
    def profile_img_tag(self):
        return format_html('<img src="/media/{}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;" />'.format(self.profile_pic))


# model for post
class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField()
    content_image = models.ImageField(upload_to='post_images', null=True, blank=True)
    content_file = models.FileField(upload_to='files', null=True, blank=True)
    likers = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    savers = models.ManyToManyField(User, related_name='saved_posts', blank=True)
    # comments = models.ManyToManyField(Comment, related_name='post_comments', blank=True)

    def __str__(self):
        return f"{self.creator.username}'s post ({self.date_created})"
    

# model for comment in post
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.post}"
    


# Models for Article Section

# Model for category of article
class Category(models.Model):
    cat_title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/')
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.cat_title
    
    def image_tag(self):
        return format_html("<img src='/media/{}' style='width:40px; height:40px; border-radius:50%' /> ".format(self.image))


# Model for post of article
class ArticlePost(models.Model):
    art_maker = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = HTMLField()
    date_created = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    







 

