from django.forms import ModelForm
from .models import Post
from django import forms

# создаём модельную форму
class NewsForm(ModelForm):
    class Meta: 
        model = Post  # это модель, по которой будет строиться форма
        # поля, которые будут выводиться на страничке
        fields = ['postAuthor', 'heading', 'text_Post', 'categoryType']
       

