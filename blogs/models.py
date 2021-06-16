from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.title} : by {self.author.first_name} {self.author.last_name}"