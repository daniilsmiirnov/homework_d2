from django.urls import path
from .views import * # импортируем наше представление
from .views import subscribe_to_category, unsubscribe_from_category
from .views import AppointmentView
 
urlpatterns = [
    # path -- означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', NewsList.as_view(), name='news'), # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>/', PostList.as_view(), name='news_detail'),
 #   path('<int:pk>/', PostList.as_view()),
    path('pag',News.as_view()),
    path('add/',NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='edit_post_form'), # Новый маршрут
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='delete_post_form'),
    path('make_app/', AppointmentView.as_view(), name='make_app'),
    #path('category/<int:pk>', PostCategoryView.as_view(), name='category'), # Ссылка на категории
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'), # Ссылка на подписчиков
    path('unsubscribe/<int:pk>', unsubscribe_from_category, name='unsubscribe'), # Ссылка на отписку
    #path('news_copy/',News.as_view())
]