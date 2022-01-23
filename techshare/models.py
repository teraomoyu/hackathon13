from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser


# Create your models here.
class Post(models.Model):
   content = models.TextField(null=False,blank=False)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   file = models.FileField(null=True,blank=True,upload_to="uploads/")
   #like追加
   like = models.ManyToManyField(User, related_name='related_post', blank=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

#    def __str__(self):
#        return self.title

   class Meta:
       ordering = ["-created_at"]     #投稿順にクエリを取得

class Comment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   comment_content = models.TextField()
   time_start = models.PositiveIntegerField()  # 時刻を秒で表示,PositiveSmallIntegerFieldなら９時間くらいは表せる
   time_end = models.PositiveIntegerField()
   position_x = models.FloatField()
   position_y = models.FloatField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Connection(models.Model):
   follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followee')
   followee = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')
   class Meta:
       unique_together = ('follower', 'followee')

   def __str__(self):
       return self.follower.username

class User(AbstractBaseUser):
    followees = models.ManyToManyField(
        'User', verbose_name='フォロー中のユーザー', through='Connection',
        related_name='+', through_fields=('follower', 'followee')
    )
    followers = models.ManyToManyField(
        'User', verbose_name='フォローされているユーザー', through='Connection', 
        related_name='+', through_fields=('followee', 'follower')
    )

'''Add'''
class VideoContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    upload_date = models.DateTimeField()
    original_name = models.CharField(max_length=200)
    filename = models.CharField(max_length=200, default="")
    #thumb_frame = models.IntegerField(default=0)

class VideoTagName(models.Model):
    name = models.CharField(max_length=200, default="")

class VideoTagList(models.Model):
    content = models.ForeignKey(VideoContent, on_delete=models.CASCADE)
    tag = models.ForeignKey(VideoTagName, on_delete=models.CASCADE)


