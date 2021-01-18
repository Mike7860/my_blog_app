from django.db import models
from django.contrib.auth.models import User
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
# from django.utils.encoding import python_2_unicode_compatible
from six import python_2_unicode_compatible


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

# class Like(models.Model):
#     quantity = models.CharField(max_length=20)


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # creating relations between posts and categories
    categories = models.ManyToManyField('Category', related_name='posts')
    liked = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=100, default='', blank=True, editable=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return str(self.title)

    @property
    def number_of_likes(self):
        # return self.liked.count()
        return self.liked

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title
        return super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # creating relations "many (comments) to one (post)"
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    liked = models.IntegerField(default=0)

    def __str__(self):
        return str(self.author)

    @property
    def number_of_likes(self):
        # return self.liked.count()
        return self.liked


blog_view = models.IntegerField(default=0)
