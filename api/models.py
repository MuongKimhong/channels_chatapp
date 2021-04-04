from django.contrib.auth.models import User, AbstractUser
from django.utils.text import slugify
from django.db import models

import uuid

class User(AbstractUser):
    code = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.code = str(uuid.uuid4())[:5]
        super(User, self).save(*args, **kwargs)


class Chatroom(models.Model):
    user_1 = models.ForeignKey(
        User, related_name='user1', on_delete=models.CASCADE, blank=True, null=True
    )
    user_2 = models.ForeignKey(
        User, related_name='user2', on_delete=models.CASCADE, blank=True, null=True
    )
    name         = models.CharField(max_length=200)
    slug         = models.SlugField()
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Chatroom, self).save(*args, **kwargs)


class Message(models.Model):
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE, blank=True, null=True)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE, blank=True, null=True)
    text   = models.TextField(blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)



