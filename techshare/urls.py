from django.urls import path
from .views import SignUpView, Home
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'video'
urlpatterns = [
    #path('detail/<int:pk>', DetailView.as_view(), name='detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', views.index, name='index'), # add
    path('', Home.as_view(), name='home')
]

#urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)