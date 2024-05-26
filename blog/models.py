from django.db import models # type: ignore
from django.urls import reverse # type: ignore

class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField(default='Default body text')
    tag = models.ManyToManyField('Tag')

    def __str__(self) :
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.id])
    


class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=20)
    message = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name