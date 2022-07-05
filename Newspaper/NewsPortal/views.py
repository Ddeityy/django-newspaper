from django.views.generic import *
from .models import *
from django.urls import *
from .filters import *
from .forms import *
from datetime import datetime
from django.contrib.auth.mixins import *
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@login_required
def author(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect('/')


@login_required
def subscribe(request, pk):
    a = request.user
    b = Category.objects.get(id=pk)
    b.subscribers.add(a)
    return redirect('/categories/')
    

class NewsList(ListView):
    model = Post
    ordering = '-creation_timedate'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    logger.info('INFO')
    
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class ProfileList(ListView):
    template_name = 'profiles.html'
    model = Author
    paginate_by = 10
    context_object_name = 'users'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = SignupForm
    success_url = '/'


class ProfileDetail(DetailView):
    model = Author
    template_name = 'profile.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SearchView(ListView):
    template_name = 'search.html'
    model = Post
    ordering = '-creation_timedate'
    paginate_by = 10

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

class Categories(ListView):
    template_name = 'categories.html'
    model = Category
    ordering = 'name'
    context_object_name = 'categories'
    

class PostDetail(DetailView):
    
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'

    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProfile(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = Author
    template_name = 'edit_user.html'
    success_url = reverse_lazy('users')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'author').exists()
        return context   


class PostDelete(DeleteView):
    form_class = PostForm
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post', 'NewsPortal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')
    def form_valid(self, form):
        post = form.save()
        post.categoryType = 'N'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post', 'NewsPortal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'A'
        return super().form_valid(form)
        
        
class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.add_post', 'NewsPortal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

