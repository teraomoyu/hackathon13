from django.urls import path
from .views import SignUpView, Home
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'video'
urlpatterns = [
    #path('detail/<int:pk>', DetailView.as_view(), name='detail'),
    path('<int:page>', views.index, name='index'),
#    path('tag/<str:tag_name>', views.tag, name='tag'),
#    path('tag/<str:tag_name>/<int:page>', views.tag, name='tag'),
#    path('search/', views.search_post, name='search'),
#    path('search/<str:search_word>', views.search, name='search'),
#    path('search/<str:search_word>/<int:page>', views.search, name='search'),
#    path('watch/<int:content_id>/', views.watch, name='watch'),
#    path('upload/', views.UploadView.as_view(), name='upload'),
#    path('edit/<int:content_id>', views.edit, name='edit'),
#    path('edit/<int:content_id>/thumb/<int:frame>', views.thumb, name='thumb'),
#    path('delete/<int:pk>', views.DeleteView.as_view(), name='delete'),
#    path('update/<int:content_id>', views.update, name='update'),
#    path('update/tag/<int:content_id>', views.update_add_tag, name='update_add_tag'),
#    path('update/tag/<int:content_id>/<str:tag_name>', views.update_remove_tag, name='update_remove_tag'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', views.index, name='index'), # add
    path('', Home.as_view(), name='home')
]

#urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)