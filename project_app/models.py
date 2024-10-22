from django.db import models
from hasnat_app.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/project_pic/')
    description = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects')
    def __str__(self):
        return self.name