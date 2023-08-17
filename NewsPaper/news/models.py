from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class Author(models.Model):
    rating_Author=models.IntegerField(default=0)
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating_Post'))
        pRating = 0
        pRating += postRat.get('postRating')

        commentRat = self.users.comment_set.all().aggregate(commentRating=Sum('rating_Comment'))
        cRating = 0
        cRating += commentRat.get('commentRating')

        self.rating_Author = pRating * 3 + cRating
        self.save()
    
class Category(models.Model):
    category = models.CharField(max_length=255,unique=True)
    
class Post(models.Model):
    heading=models.CharField(max_length=255)
    text_Post = models.TextField()
    rating_Post=models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    postCategory= models.ManyToManyField(Category, through='PostCategory')
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    def like(self):
        self.rating_Post+=1
        self.save()
    
    def dislike(self):
        self.rating_Post-=1
        self.save()
    def preview(self):
        return self.text_Post[0:124] + '...'
        
        
    
    
class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    
class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text_Comment = models.TextField()
    date_Comment = models.DateTimeField(auto_now_add=True)
    rating_Comment = models.IntegerField(default=0)
    def like(self):
        self.rating_Comment+=1
        self.save()
    def dislike(self):
        self.rating_Comment-=1
        self.save()