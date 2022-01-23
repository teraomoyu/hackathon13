from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView
from django.contrib.auth import authenticate,login,logout

from .models import Post
from .forms import SignUpForm
from .models import VideoContent, VideoTagList, VideoTagName

from django.db.models import Count


def construct_page(request, all_content_ids, page_contents, current_page, max_page, url_type, url_word=''):
    # page_contents(動画)に関連するタグを抜き出し、テンプレートで使えるよう整形
    contents = []
    for item in page_contents:
        tmp_dict = item
        tmp_dict.update({'tags': VideoTagList.objects.filter(content_id=item['id']).select_related('tag')})
        contents.append(tmp_dict)

    # all_content_idsからタグを多い順で集計し、整形する
    tag_cnt = VideoTagList.objects.filter(content__in = all_content_ids).values('tag').annotate(tag_count=Count('tag')).order_by('-tag_count')[:10]
    tag_names = [VideoTagName.objects.filter(id = item.get('tag'))[0] for item in tag_cnt]
    tags = [{'name': tag_names[i].name, 'count': tag_cnt[i]["tag_count"]} for i in range(len(tag_names))]

    # ページが有効な範囲をvalidでマークを付ける
    page_list = [{'num':x, 'valid':0 <= x and x <= max_page} for x in range(current_page-5, current_page+4)]

    return render(request, 'video/index.html', {'tags': tags, 'contents': contents, 'page':{'type':url_type, 'word': url_word, 'current': current_page, 'max': max_page, 'list': page_list}})

def index(request, page=0):
    max_page = VideoContent.objects.count() // 10
    return construct_page(request, VideoTagList.objects.values('content_id'), VideoContent.objects.order_by('-upload_date')[page*10:(page+1)*10].values(), page, max_page, 'video:index')

def tag(request, tag_name, page=0):
    # tag_nameからIDを探し、見つかったIDを基にタグが付いた動画をフィルタする
    tag_id = VideoTagName.objects.filter(name=tag_name).get().id
    filtered_list = VideoTagList.objects.select_related('content').filter(tag=tag_id).order_by('-content__upload_date')

    max_page = filtered_list.count() // 10

    content_list = filtered_list[page*10:(page+1)*10]
    contents = [{'id':item.content.id, 'title':item.content.title} for item in content_list]

    return construct_page(request, filtered_list.values('content_id'), contents, page, max_page, 'video:tag', tag_name)

def search(request, search_word, page=0):
    filtered_list = VideoContent.objects.filter(title__contains=search_word).order_by('-upload_date')
    max_page = filtered_list.count() // 10
    content_list = filtered_list[page*10:(page+1)*10]
    contents = [{'id':item.id, 'title':item.title} for item in content_list]

    return construct_page(request, filtered_list.values('id'), contents, page, max_page, 'video:search', search_word)

def search_post(request):
    if hasattr(request, 'POST') and 'search_text' in request.POST.keys():
        if request.POST['search_text'] != "":
            return HttpResponseRedirect(reversed('video:search', args=(request.POST['search_text'],)))

    return HttpResponseRedirect(reversed('video:index'))

#def index(request):
 #   return render(request, 'video/index.html')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()  # フォームの内容を保存
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

# class LoginView(CreateView):
#     template_name = 'login.html'
#     form_class = LoginForm
#     success_url = reverse_lazy('home')


#     def get(self,request):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
    
#     def post(self, request):
#         # pass filled out HTML-Form from View to LoginForm()
#         form_class = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 # create a new entry in table 'logs'
#                 login(request, user)
#                 print('success login')
#                 return HttpResponseRedirect('/')
#             else:
#                 return HttpResponseRedirect('login')
#         return HttpResponse('This is Login view. POST Request.')
    



class Home(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'

    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user)

#class DetailPost(LoginRequiredMixin, DetailView):
 #   model = Post
  #  template_name = 'detail.html'


# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import generic
from django import forms
from django.core.files.storage import default_storage, FileSystemStorage
from django.utils import timezone
from django.conf import settings

import ffmpeg

DATA_DIR = str(settings.MEDIA_ROOT) + 'video/'

def edit(request, content_id):
    return HttpResponse("dummy")

def delete_video(content_id, video_filename):
    print('remove files at ' + str(content_id) + '/')
    storage = FileSystemStorage()
    storage.location = DATA_DIR
    storage.delete(str(content_id) + '/' + video_filename)
    storage.delete(str(content_id) + '/' + 'thumb.jpg')
    storage.delete(str(content_id) + '/')


def make_video_thumb(src_filename, capture_frame, dst_filename=None):
    probe = ffmpeg.probe(src_filename)
    video_info = next(x for x in probe['streams'] if x['codec_type'] == 'video')
    nframes = video_info['nb_frames']
    avg_frame_rate = (lambda x: int(x[0])/int(x[1])) (video_info['avg_frame_rate'].split('/'))
    start_position = int(capture_frame)/avg_frame_rate

    if dst_filename == None:
        out_target = 'pipe:'
    else:
        out_target = dst_filename

    im = (
        ffmpeg.input(src_filename, ss=start_position)
        .filter('scale', 200, -1)
        .output(out_target, vframes=1, format='image2', vcodec='mjpeg', loglevel='warning')
        .overwrite_output()
        .run(capture_stdout=True)
    )

    return im


class VideoUploadForm(forms.Form):
    file = forms.FileField()

class UploadView(generic.FormView):
    form_class = VideoUploadForm
    template_name = 'video/upload.html'

    def form_valid(self, form):
        upload_filename = form.cleaned_data["file"].name

        content = VideoContent(title=upload_filename, description="", upload_date=timezone.now(), original_name=upload_filename, filename="")
        content.save()

        try:
            storage = FileSystemStorage()
            storage.location = DATA_DIR + str(content.id)
            filename = storage.save(upload_filename, form.cleaned_data["file"])
            make_video_thumb(DATA_DIR + str(content.id) + "/" + filename, content.thumb_frame, DATA_DIR + str(content.id) + "/thumb.jpg")

        except:
            delete_video(content.id, filename)
            content.delete()
            raise

        else:
            content.filename = filename
            content.save()

            return HttpResponseRedirect(reverse('video:edit', args=(content.id,)))

def edit(request, content_id):
    content = get_object_or_404(VideoContent, pk=content_id)

    probe = ffmpeg.probe(DATA_DIR + str(content.id) + "/" + content.filename)
    video_info = next(x for x in probe['streams'] if x['codec_type'] == 'video')
    info = {'max_frame': video_info['nb_frames']}

    tags = VideoTagList.objects.filter(content_id=content_id).select_related('content')

    return render(request, 'video/edit.html', {'content':content, 'video_info':info, 'tags':tags})


def thumb(request, content_id, frame):
    content = get_object_or_404(VideoContent, pk=content_id)
    im = make_video_thumb(DATA_DIR + str(content.id) + "/" + content.filename, frame)
    return HttpResponse(im, content_type="image/jpeg")


def update(request, content_id):
    content = get_object_or_404(VideoContent, pk=content_id)
    content.title = request.POST['title']
    content.thumb_frame = request.POST['frame']
    content.description = request.POST['desc']
    content.save()

    make_video_thumb(DATA_DIR + str(content.id) + "/" + content.filename, content.thumb_frame, DATA_DIR + str(content.id) + "/thumb.jpg")

    return HttpResponseRedirect(reverse('video:index'))

def update_add_tag(request, content_id):
    if request.POST["tag"] != "":
        tag = VideoTagName.objects.filter(name=request.POST["tag"])
        if len(tag) == 0:
            tag = VideoTagName(name=request.POST["tag"])
            tag.save()
        else:
            tag = tag[0]

        tag_list = VideoTagList.objects.filter(tag_id=tag.id, content_id=content_id)
        if len(tag_list) == 0:
            tag_list = VideoTagList(tag_id=tag.id, content_id=content_id)
            tag_list.save()

    return HttpResponseRedirect(reverse('video:edit', kwargs={'content_id': content_id}))

def update_remove_tag(request, content_id, tag_name):
    tag = VideoTagName.objects.filter(name=tag_name)
    if len(tag) != 0:
        tag_list = VideoTagList.objects.filter(tag_id=tag[0].id, content_id=content_id)
        tag_list.delete()

    return HttpResponseRedirect(reverse('video:edit', kwargs={'content_id': content_id}))

class DeleteView(generic.DeleteView):
    model = VideoContent
    template_name = 'video/delete.html'
    success_url = reverse_lazy('video:index')

    def delete(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        filename = VideoContent.objects.filter(id=content_id)[0].filename
        delete_video(content_id, filename)

        return super().delete(request, *args, **kwargs)
