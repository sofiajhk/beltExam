from __future__ import unicode_literals
from django.db import models
from time import gmtime, strftime
import datetime
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    # basic validations for registering
    def register_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[\w\.+_-]+@[\w\._-]+\.[\w]*$')
        errors = []

        if len(postData['first_name']) <= 2 or len(postData['last_name']) <= 2:
            errors.append("Name field is required and must be at least 3 characters!")
        elif postData['first_name'].isalpha() == False or postData['last_name'].isalpha() == False:
            errors.append("Name field can only contain letters!")
        
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email is not valid!")
        elif len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("Email already exists!")

        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")
        elif postData['password'] != postData['pw_conf']:
            errors.append("Password and Confirmation Password do not match!")
        
        if errors:
            return errors
        else:
            # if there are no errors, hash pw and create user
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = self.create(
                first_name = postData['first_name'],
                last_name = postData['last_name'],
                email = postData['email'],
                password = hashed_pw
            )
            return new_user

    # basic validations for log-in
    def login_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[\w\.+_-]+@[\w\._-]+\.[\w]*$')
        errors = []

        email = postData['email']
        password = postData['password']

        if not EMAIL_REGEX.match(email):
            errors.append("Email is not valid")

        if len(password) < 8:
            errors.append("Password is not valid")

        # if no errors, check the db for user info
        if not errors:
            try:
                # checking if user in db
                user = self.get(email = postData['email'])
                hashed_pw = user.password
                bcrypt.checkpw(postData['password'].encode(), hashed_pw.encode())
                return user
            except:
                errors.append('Invalid username or password')
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "<User object: Name: {} {} \nEmail: {} \nCreated: {} \nUpdated: {}>".format(self.first_name, self.last_name, self.email, self.created_at, self.updated_at)

    objects = UserManager()