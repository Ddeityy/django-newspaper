"""Newspaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from NewsPortal.views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', RedirectView.as_view(url='http://127.0.0.1:8000/news/')),
    path('admin/', admin.site.urls),
    
    path('news/', cache_page(60)(NewsList.as_view()), name='news_list'),
    path('news/<int:pk>', cache_page(60*10)(PostDetail.as_view()), name='post_detail'),
    
    path('categories/', Categories.as_view(), name='post_detail'),
    path('categories/subscribe/<int:pk>/', subscribe, name='subscribe'),
    
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),   
    
    path('news/search/', SearchView.as_view(), name='search'),
    
    path('users/', ProfileList.as_view(), name='users'),
    path('users/<int:pk>', ProfileDetail.as_view(), name='profile_detail'),
    path('users/<int:pk>/edit', EditProfile.as_view(), name='edit_user'),
    
    path('accounts/', include('allauth.urls')),
    path('account/', IndexView.as_view(), name = 'index'),
    path('account/logout/', LogoutView.as_view(template_name = 'account/logout.html'), name='logout'),
    path('account/login/', LoginView.as_view(template_name = 'account/login.html'), name='login'),
    path('account/signup/', BaseRegisterView.as_view(template_name = 'account/signup.html'), name='signup'),
    path('account/author/', author, name = 'author'),
]
