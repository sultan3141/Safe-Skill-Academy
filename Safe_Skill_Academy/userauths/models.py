from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    refresh_token=models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # still required when creating superuser

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        email_username = self.email.split('@')[0]
        if not self.full_name:  # handles both "" and None
            self.full_name = email_username
        if not self.username:
            self.username = email_username
        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_folder', default="default-user.jpg", blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name if self.full_name else self.user.email

    def save(self, *args, **kwargs):
        # Derive username from email if needed
        email_username = self.user.email.split('@')[0]
        if not self.full_name:
            self.full_name = email_username
        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Assuming you have a Profile model linked to the User model
        Profile.objects.create(user=instance)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()        
post_save.connect(create_user_profile, sender=User)  
post_save.connect(save_user_profile, sender=User)
  
