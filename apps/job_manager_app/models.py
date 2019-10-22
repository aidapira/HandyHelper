from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, timedelta, date
import math


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "User's first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "User's last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "User's password should be at least 8 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pw'] = "Password does not match"
        return errors

    def jobmanager(self, postData):
        errors = {}
        if 0 < len(postData['job']) < 3:
            errors["job"] = "Job should be at least 3 characters"
        if 0 < len(postData['description']) < 3:
            errors["description"] = "Description should be at least 3 characters"
        if 0 < len(postData['location']) < 3:
            errors["location"] = "Location should be at least 3 characters"
        if len(postData['job']) == 0:
            errors["job"] = "A job must be provided!"
        if len(postData['description']) == 0:
            errors["description"] = "A description must be provided!"
        if len(postData['location']) == 0:
            errors["location"] = "A location must be provided!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Job(models.Model):
    job = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="jobs")
    isadded = models.BooleanField(default=False)
    objects = UserManager()

class Category(models.Model):
    categories = models.ManyToManyField(Job, related_name="categories")
