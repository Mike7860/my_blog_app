from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    #creating relations between posts and categories
    categories = models.ManyToManyField('Category', related_name='posts')


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # creating relations "many (comments) to one (post)"
    post = models.ForeignKey('Post', on_delete=models.CASCADE)