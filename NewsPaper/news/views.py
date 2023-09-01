from django.views.generic import ListView, DetailView, UpdateView, CreateView,DeleteView
from .models import *
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.urls import reverse_lazy

class NewsList (ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by= 3
    queryset = Post.objects.order_by('-date')
    form_class= NewsForm
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
       context = super().get_context_data(**kwargs)
       #context['categories'] = PostCategory.objects.all()
       #context['postAuthor'] = Author.objects.all()
       context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
       context['choices'] = Post.CATEGORY_CHOICES
       context['form'] = NewsForm()
       return context
    def post(self, request, *args, **kwargs):
       form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса
       if form.is_valid():
           form.save()
       return super().get(request, *args, **kwargs)
class NewsDetailView(DetailView):
   template_name = 'newspaper/news_detail.html'
   queryset = Post.objects.all()

class NewsCreateView(CreateView):
   template_name = 'newspaper/news_create.html'
   form_class = NewsForm
class NewsUpdateView(UpdateView):
    model = Post
    context_object_name = 'edit_post_form'
    template_name = 'newspaper/news_create.html'
    form_class=NewsForm
    #fields = ('header', 'body')
    def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)
    #success_url = reverse_lazy(viewname='post_list')
# удаление поста
class NewsDeleteView(DeleteView):
    model = Post
    context_object_name = 'delete_post_form'
    template_name = 'newspaper/news_delete.html'
    queryset = Post.objects.all()
    #fields = ('header', 'post_date')
    success_url = reverse_lazy('news')
class PostList(DetailView):
    model = Post
    template_name= 'post.html'
    context_object_name = 'posts'   

class News(View):
    
    def get(self, request):
        news = Post.objects.all()
        p = Paginator(news, 2) # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
 
        news = p.get_page(request.GET.get('page', 1)) # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами
        
        data = {
            'news': news,
        }
        return render(request, 'news copy.html', data)