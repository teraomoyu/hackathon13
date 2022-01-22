from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

from .models import Post
from .forms import SignUpForm,LoginForm,PostForm,CommentForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

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

class DetailPost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'detail.html'


# Create your views here.
