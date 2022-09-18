from django.shortcuts import render, redirect   
from django.http import HttpResponse ,HttpResponseRedirect
from .models import Post
from django.contrib import messages
from django.db.models import Q


from django.shortcuts import render
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
#from django.http import HttpResponse

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blogapp/home.html',context)


class PostListView(ListView):
    model = Post
    template_name = 'blogapp/home.html'  # <app>/<model>_<viewtype>.html
    

    context_object_name ='posts'
    ordering = ['-date_posted']  #to order by most recent one


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):  #loginrequiredmixin class is inherited so that user is able to post only when he is logged in
    model = Post   #LoginRequiredMixin is used similar to as we used decorator for function based views, in class based we cannot use decorator
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#UserPassesTestMixin is used to check that only author of that post should be able to update that post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post  
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  # this function is run by UserPassesTestMixin
        post = self.get_object()  # get object gets the current post
        if self.request.user == post.author:  # to check author is updating
            return True  # allow
        return False

#UserPassesTestMixin is used to check that only author of that post should be able to delete that post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  #after deletion it is redirected to home

    def test_func(self):  # this function is run by UserPassesTestMixin
        post = self.get_object() #get object gets the current post
        if self.request.user == post.author:  #to check author is updating
            return True                       #allow
        return False



def about(request):
    return render(request, 'blogapp/about.html', {'title': 'About'})
def login(request):
    return render(request,'blogapp/login.html')
def profile(request):
    return render(request,'blogapp/profile.html')
def logout(request):
    return render(request,'blogapp/logout.html')
def register(request):
    return render(request,'blogapp/register.html')
def blogsearch(request):
    if request.method=='POST':
        search = request.POST['search']

        if search:
            match=Post.objects.filter(Q(title__icontains=search)|Q(content__icontains=search)|Q(author__icontains=search))

            if match :
                return render(request ,'home.html',{'search':match})
            else:     
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('/blogSearch/')
    return render(request, 'home.html')
 
