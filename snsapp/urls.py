from django.urls import path
from .views import Home, MyPost,DetailPost,CreatePost,DeletePost,UpdatePost, LikeHome, LikeDetail, FollowHome, FollowDetail, FollowList      #追加


urlpatterns = [
   path('', Home.as_view(), name='home'),             #追加
   path('mypost/', MyPost.as_view(), name='mypost'),  #追加
   path('detail/<int:pk>', DetailPost.as_view(), name='detail'), #追加
   path('detail/<int:pk>/update', UpdatePost.as_view(), name='update'), #追加
   path('detail/<int:pk>/delete', DeletePost.as_view(), name='delete'), #追加
   path('create/', CreatePost.as_view(), name='create'),      #追加
   path('like-home/<int:pk>', LikeHome.as_view(), name='like-home'),
   path('like-detail/<int:pk>', LikeDetail.as_view(), name='like-detail'),
      path('follow-home/<int:pk>', FollowHome.as_view(), name='follow-home'),
   path('follow-detail/<int:pk>', FollowDetail.as_view(), name='follow-detail'),
   path('follow-list/', FollowList.as_view(), name='follow-list'),
]