from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import *


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)
    age = models.IntegerField(default=18)
    
    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum("rating"))
        pRat = 0
        pRat += postRat.get("postRating")
        
        commnetRat = self.authorUser.comment_set.aggregate(commentRating=Sum("rating"))
        cRat = 0
        cRat += commnetRat.get("commentRating")
        
        self.authorRating = pRat *3 + cRat
        self.save()
    
    def __str__(self):
        return f'{self.authorUser} - {self.age}'


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
    сategoryType = models.CharField(max_length=1, choices=CATEGORY_CHOICE, default=ARTICLE)
    creation_timedate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through="PostCategory")
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
    
    def get_absolute_url(self):
        return reverse("article", args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.postThrough}: {self.categoryThrough}'


class Comment(models.Model):
    
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
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
        return f'Comment by {self.commentUser} on {self.commentPost}'