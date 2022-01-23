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
