from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import Profile
from posts.models import Post
from django_project.util import unique_slug_generator

# Creates Profile instance as soon as a user is created in User table
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Save profile after user has created
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# Convert title into slug, as soon as a post instance is created
@receiver(pre_save, sender=Post)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

