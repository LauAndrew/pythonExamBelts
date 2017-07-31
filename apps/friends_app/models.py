from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['name']) < 3:
            errors['name'] = "Name must be at least 3 characters long"
        if len(post_data['alias']) < 3:
            errors['alias'] = "Alias must be at least 3 characters long"
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = 'Email is not valid'
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if post_data['password'] != post_data['confirm_pw']:
            errors['password'] = "Password must match password confirmation field"
        return errors

    def addFriend(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        Friend.objects.create(user_friend=user, second_friend=friend)
        Friend.objects.create(user_friend=friend, second_friend=user)

    def removeFriend(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        friendship1 = Friend.objects.get(user_friend=user, second_friend=friend)
        friendship2 = Friend.objects.get(user_friend=friend, second_friend=user)
        friendship1.delete()
        friendship2.delete()

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Friend(models.Model):
    user_friend = models.ForeignKey(User, related_name='requesting')
    second_friend = models.ForeignKey(User, related_name='accepting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
