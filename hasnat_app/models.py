from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('developer', 'Developer'),
        ('manager', 'Manager'),
        ('qa', 'QA')
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
   
    email = models.EmailField(blank=True, null=True, unique=True)  

    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username
 

class Project(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/project_pic/')

    description = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects')
   
    def __str__(self):
        return self.name

class Screenshot(models.Model):
    bug = models.ForeignKey('Bug', related_name='screenshots', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bug_screenshots/')

    def __str__(self):
        return f'Screenshot {self.id} for Bug {self.bug.title}'


class Bug(models.Model):
    BUG_TYPE_CHOICES = [
        ('feature', 'Feature'),
        ('bug', 'Bug')
    ]
    STATUS_CHOICES_BUG = [
        ('new', 'New'),
        ('started', 'Started'),
        ('resolved', 'Resolved')
    ] 

    STATUS_CHOICES_FEATURE = [
        ('new', 'New'),
        ('started', 'Started'),
        ('completed', 'Completed')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    type = models.CharField(max_length=200, choices=BUG_TYPE_CHOICES)
    status = models.CharField(max_length=200, choices=[], default='new' )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bugs')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_bugs')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_bugs')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        if self.type == 'bug':
            self._meta.get_field('status').choices = self.STATUS_CHOICES_BUG
            self.required=False
        else:
            self._meta.get_field('status').choices = self.STATUS_CHOICES_FEATURE
            self.required=False

    def save(self, *args, **kwargs):
        if self.type == 'bug':
            self._meta.get_field('status').choices = self.STATUS_CHOICES_BUG
            self.required=False
        else:
            self._meta.get_field('status').choices = self.STATUS_CHOICES_FEATURE
            self.required=False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
