from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    birth = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return 'user{}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    company = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    about_me = models.TextField(blank=True)

    def __str__(self):
        return "user{}".format(self.user.username)



