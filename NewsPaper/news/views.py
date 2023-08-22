from django.views.generic import ListView, DetailView
from .models import *


class NewsList (ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    
class PostList(DetailView):
    model = Post
    template_name= 'post.html'
    context_object_name = 'posts'