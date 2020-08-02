from django.db import models
import re													
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')							
							
class UserManager(models.Manager):
    def register(self, postData):
        pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode() # create the hash 
        return self.create(
            first_name=postData['first_name'], 
            last_name=postData['last_name'], 
            birth_date=postData['birth_date'], 
            email=postData['email'], 
            password=pw_hash
        )
    # Checking login 
    def authenticate(self, email, password):
        user_with_email = self.filter(email = email)
        if not user_with_email: # we quering for all users with this email, and if its empty list:
            return False
        user = user_with_email[0] # if we do have user with that email in our system:
        return bcrypt.checkpw(password.encode(), user.password.encode()) # checkpw returns True of False

    def validator(self, postData):												
        errors = {}																										
        # NAME VALIDATION 	
        if len(postData['first_name']) < 2:											
            errors['first_name'] = 'First name should be atleast 2 characters long.'	
        if not postData['first_name'].isalpha() and postData['first_name'] != '':
            errors['first_name'] = 'First name must containt only letters.'
        if len(postData['last_name']) < 2:										
            errors['last_name'] = 'Last name should be atleast 2 characters long'
        if not postData['last_name'].isalpha() and postData['first_name'] != '':
            errors['last_name'] = 'Last name must containt only letters.'
        # DATE VALIDATION
        if len(postData['birth_date']) < 1:	                							
            errors['birth_date'] = 'Birth date required.'
        else: 
            current_date = datetime.now()                                              
            date_from_form = postData['birth_date']
            converted_date_from_form = datetime.strptime(date_from_form, "%Y-%m-%d")
            duration = current_date - converted_date_from_form
            age = duration.days / 365.25
            if age < 13:										
                errors['birth_date'] = 'User must be older then 13 years.'	
            if datetime.strptime(postData['birth_date'], '%Y-%m-%d') > datetime.now():
                errors['birth_date'] = 'Date of birth should be in the past.'  
        # EMAIL VALIDATION
        if len(postData['email']) < 1:
            errors['email'] = "Email cannot be blank."
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Email is not valid"
        result =  self.filter(email = postData['email'])
        if len(result) > 0:
            errors['email'] = "Email is already registered."
        # PASSWORD VALIDATION
        if len(postData['password']) < 3:
            errors['password'] = 'Password required, should be atleast 8 characters long.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Confirmation didn't match the password"
        return errors

class JobManager(models.Manager):
    def job_validator(self, postData):												
        errors = {}																										
        # NAME VALIDATION 	
        if len(postData['description']) < 4:											
            errors['description'] = 'A job must consist of at least 3 characters'
        if len(postData['location']) == 0:											
            errors['location'] = 'Location must be provided.'	
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)										
    last_name = models.CharField(max_length = 255)										
    birth_date = models.DateTimeField()											
    email = models.TextField()
    phone_num = models.IntegerField(blank=True, null = True)
    about = models.TextField(blank=True, null = True)	
    password = models.TextField()								
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)									
    objects = UserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Job(models.Model):
    title = models.CharField(max_length = 255, null = True)
    description = models.TextField()
    location = models.CharField(max_length = 255)
    poster = models.ForeignKey(User, related_name = 'poster', on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name = 'executor', on_delete=models.CASCADE, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)	
    objects = JobManager()
    #categories
    #comments
    def __str__(self):
        return self.title
class Category(models.Model):
    name = models.CharField(max_length = 255)
    job = models.ManyToManyField(Job, related_name = 'categories')
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.name


class Comment(models.Model):
    comment = models.TextField(default = 'Hello')
    poster = models.ForeignKey(User, related_name = 'comments', on_delete=models.CASCADE) # Comments has a poster, User has comments
    job = models.ForeignKey(Job, related_name = 'comments', on_delete=models.CASCADE) # message where comment was posted on. Message has comments, but comment belongs to one message 
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)	
    def __str__(self):
        return f"{self.poster.first_name} {self.poster.last_name}: {self.comment}"