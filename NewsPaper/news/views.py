from django.views.generic import ListView, DetailView, UpdateView, CreateView,DeleteView
from .models import *
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
 
from .models import Appointment
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

class NewsCreateView(CreateView,PermissionRequiredMixin):
   template_name = 'newspaper/news_create.html'
   form_class = NewsForm
   permission_required = ('news.add_post', )
class NewsUpdateView(LoginRequiredMixin,UpdateView,PermissionRequiredMixin):
    model = Post
    context_object_name = 'edit_post_form'
    template_name = 'newspaper/news_create.html'
    form_class=NewsForm
    #fields = ('header', 'body')
    def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)
    #success_url = reverse_lazy(viewname='post_list')
    permission_required = ('news.change_post', )
# удаление поста
class NewsDeleteView(DeleteView,PermissionRequiredMixin):
    model = Post
    context_object_name = 'delete_post_form'
    template_name = 'newspaper/news_delete.html'
    queryset = Post.objects.all()
    #fields = ('header', 'post_date')
    success_url = reverse_lazy('news')
    permission_required = ('news.delete_post', )
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
    
@login_required
def subscribe_to_category(request, pk):  # подписка на категорию
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Подписка на {category} на сайте News Paper',
            body='',
            from_email=DEFAULT_FROM_EMAIL, #  в settings.py
            to=[email, ], # список получателей
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))
        #return redirect('news_list')
    return redirect(request.META.get('HTTP_REFERER'))  # возвращает на страницу, с кот-й поступил запрос


@login_required
def unsubscribe_from_category(request, pk):  # отписка от категории
    user = request.user
    c = Category.objects.get(id=pk)

    if c.subscribers.filter(id=user.id).exists():  #проверяем есть ли у нас такой подписчик
        c.subscribers.remove(user) # то удаляем нашего пользователя
    #return redirect('http://127.0.0.1:8000/')
    return redirect(request.META.get('HTTP_REFERER'))





class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'newspaper/make_app.html', {})
 
    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()
 
        return redirect('newspaper:make_app')
        return redirect('appointments:make_appointment')