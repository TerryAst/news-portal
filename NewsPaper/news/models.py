from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default = 0)
    def update_rating(self, rating_to_update):
        
        # Подсчет рейтинга постов пользователя.
        
        list_rating_of_posts = Post.objects.filter(author_post=self.user).values('rating')
        sum_rating_of_posts = 0
        for i in range(len(list_rating_of_posts)):
            sum_rating_of_posts += i.rating     
        sum_rating_of_posts = sum_rating_of_posts * 3
        
        # Подсчет рейтинга комментариев пользователя.
             
        list_rating_of_comments = Comment.objects.filter(comment_of_user=self.user).values('rating_comment')
        sum_rating_of_comments = 0
        for y in range(len(list_rating_of_comments)):
            sum_rating_of_comments += y.rating    
        
        # Подсчет рейтинга комментариев к статьям пользователя
        
        list_rating_of_post_comments = Comment.objects.filter(comment_of_post__author_post=self.user).values('rating_comment')
        sum_rating_of_post_comments = 0
        for w in range(len(list_rating_of_post_comments)):
            sum_rating_of_post_comments += w.rating    
            
        # Подсчет общего рейтинга
        
        rating_to_update = sum_rating_of_posts + sum_rating_of_comments + sum_rating_of_post_comments
        
        
                

class Category(models.Model):
    category_name = models.CharField(unique = True)
      
    
class Post(models.Model):
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(choices = [{'article', 'статья'}, {'news','новость'}], 
                            default = 'article')
    date_of_creation = models.DateTimeField(auto_now_add = True)
    category_of_post = models.ManyToManyField(Category)
    header = models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=255, blank=True)
    rating = models.IntegerField(default = 0)
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()
        
    def preview(self):
        return self.text[:123]+'...'
        
     
class PostCategory(models.Model):
    postcategory_of_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    postcategory_of_category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    
class Comment(models.Model):
    comment_of_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_of_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.CharField(max_length=255, blank=True)
    date_of_comment_creation = models.DateTimeField(auto_now_add = True)
    rating_comment = models.IntegerField(default = 0)
    
    def like(self):
        self.rating_comment += 1
        self.save()
        
    def dislike(self):
        self.rating_comment -= 1
        self.save()
    