from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,DetailView,FormView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .forms import SignUpForm,LoginForm,PostForm,CommentForm

"""マウスクリックの座標を取得のために追加"""
from pynput import mouse
import pyautogui
import time
from datetime import datetime

def get_now():
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return now

def on_move(x, y):
    return

def on_click(x, y, button, pressed):
    if pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    return

#登録処理
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()  # フォームの内容を保存
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

#ログイン処理(関数型)
def login(request):
    if request.method == 'POST':
        form = AuthenticateForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f"You are now logged in as {username}")
                return redirect(self.get_success_url)
#ログアウト
def logout(request):
    logout(request)
    return redirect('/')


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

class DetailPost(LoginRequiredMixin, DetailView, FormView):  # 投稿の詳細画面
    model = Post
    template_name = 'detail.html'
    form_class = CommentForm
    success_url = reverse_lazy('detail')

    def get_context_data(self, **kwargs):  # 投稿に対応するコメントの取得
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        comment = form.save(commit=False) 
        comment.user = self.request.user
        comment.post = get_object_or_404(Post, id=self.kwargs['pk'])
        with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
            listener.join()

        x, y = pyautogui.position()
        print("zahyou", x, y)
        comment.position_x = x
        comment.position_y = y
        comment.save()
        return HttpResponseRedirect(reverse('detail', kwargs={'pk': self.kwargs['pk']}))

class MyPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'

    def get_queryset(self):
       #リクエストユーザーに限定
       return Post.objects.filter(user=self.request.user)

class BookmarkView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'

    def get_queryset(self):
       #リクエストユーザーがいいねした投稿に限定
       return Post.objects.filter(like=self.request.user)


# Create your views here.
