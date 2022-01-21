from django.db import models
from django.contrib.auth.models import User
from django.forms import FloatField

class Post(models.Model):
   content = models.TextField()
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   
   #like追加
   like = models.ManyToManyField(User, related_name='related_post', blank=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return self.title

   class Meta:
       ordering = ["-created_at"]     #投稿順にクエリを取得

class Comment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   comment_content = models.TextField()
   time = models.PositiveIntegerField()  # 時刻を秒で表示,PositiveSmallIntegerFieldなら９時間くらいは表せる
   position_x = models.FloatField()
   position_y = models.FloatField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Connection(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   following = models.ManyToManyField(User, related_name='following', blank=True)

   def __str__(self):
       return self.user.username
