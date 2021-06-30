from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class UserInfo(models.Model):
    uname = models.OneToOneField(User, on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=250)
    about = models.TextField(max_length=500)
    storprof_CHOICES =(
        ("Student", "Student"),
        ("Professional", "Professional"),
        ("Other", "Other"),
    )
    storprof = models.CharField(
        max_length=12,
        choices=storprof_CHOICES,
        default="Other",
    )
    where_do_you_work = models.CharField(max_length=50)
    graduation_year = models.IntegerField()
    blog_post = models.BooleanField(default=False)
    newletter = models.BooleanField(default=False)
    offers = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id}." + f"{self.uname}".capitalize()

class ContactForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} wants to contact us"
    
