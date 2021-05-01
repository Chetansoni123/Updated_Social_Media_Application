from django.db import models
from django.urls import reverse
from django.utils import timezone 
from django.contrib.auth.models import User

# Post model 
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    content = models.TextField()
    img = models.ImageField(default='default.jpg', upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    user_post = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
        
