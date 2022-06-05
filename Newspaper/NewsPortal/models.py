from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    authour_rating = models.SmallIntegerField(default=0)
    age = models.IntegerField(default=18)

    def update_rating(self):
        post_rat = self.post_set.aggregate(postRating=Sum("rating"))
        p_rat= 0
        p_rat+= post_rat.get("postRating")

        commnet_rat = self.author_user.comment_set.aggregate(commentRating=Sum("rating"))
        c_rat = 0
        c_rat += commnet_rat.get("commentRating")

        self.authour_rating = p_rat*3 + c_rat
        self.save()

    def __str__(self):
        return f'{self.author_user} - {self.age}'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'N'
    ARTICLE = 'A'

    CATEGORY_CHOICE = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_type = models.CharField(max_length=1, choices=CATEGORY_CHOICE, default=ARTICLE)
    creation_timedate = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through="post_category")
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def preview(self):
        return self.text[:123]+"..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def __str__(self):
        return f'{self.title.title()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    def get_absolute_url(self):
        return reverse("article", args=[str(self.id)])


class post_category(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_through}: {self.category_through}'


class Comment(models.Model):

    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_timedate = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def __str__(self):
        return f'Comment by {self.comment_user} on {self.comment_post}'
