from django.db import models
from django.contrib.auth.models import User

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True, unique=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pictures')
    
    def __str__(self):
        return f'{self.user.username} Profile'

# Friends model 
class friends(models.Model):
    conn_user = models.CharField(max_length=50)
    user_friend = models.ManyToManyField(User)

    def __str__(self):
        return self.conn_user
