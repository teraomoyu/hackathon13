from django.urls import path
from .views import SignUpView, Home, DetailView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('detail/<int:pk>', DetailView.as_view(), name='detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', Home.as_view(), name='home')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)