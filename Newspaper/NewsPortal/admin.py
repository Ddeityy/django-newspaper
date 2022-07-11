from django.contrib import admin

from .models import Author, Comment, Category, Post
from modeltranslation.admin import TranslationAdmin

admin.site.register(Author)
admin.site.register(Comment)

class CategoryAdmin(TranslationAdmin):
    model = Category

class PostAdmin(TranslationAdmin):
    model = Post

admin.site.register(Category)
admin.site.register(Post)