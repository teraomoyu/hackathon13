from django.contrib import admin
from .models import Post,Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)

from .models import VideoContent, VideoTagName, VideoTagList


class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'upload_date')

class VideoTagListAdmin(admin.ModelAdmin):
    list_display = ('content', 'tag')

class VideoTagNameAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(VideoContent, VideoContentAdmin)
admin.site.register(VideoTagList, VideoTagListAdmin)
admin.site.register(VideoTagName, VideoTagNameAdmin)