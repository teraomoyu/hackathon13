from django.urls import path
from .views import SignUpView, Home, DetailView, BookmarkView, MyPostView,login,logout
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('detail/<int:pk>', DetailView.as_view(), name='detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('bookmark/', BookmarkView.as_view(), name="bookmark"),
    path('mypost/', MyPostView.as_view(), name="mypost"),
    path('', Home.as_view(), name='home')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)