from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name='blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self,**kwargs):
        context = super(PostListView,self).get_context_data(**kwargs)
        liked = {}
        for post in context['posts']:
            liked[post.id] = post.likes.filter(id=self.request.user.id).exists()
        context['liked'] = liked
        return context

class UserPostListView(ListView):
    model = Post
    template_name='blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5 

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','image','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','image','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Post = self.get_object()
        if self.request.user == Post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = "/"
    def test_func(self):
        Post = self.get_object()
        if self.request.user == Post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def handle_like(request):
    post_id = request.GET.get('post_id', None)
    user_id = request.GET.get('user_id', None)
    post = Post.objects.filter(id=post_id).get()
    likes = post.likes.filter(id=user_id).exists()
    if(likes):
        user = post.likes.filter(id=user_id).get()
        post.likes.remove(user)
        data = {
            'like' : False
        }
    else:
        user = User.objects.filter(id=user_id).get()
        post.likes.add(user)
        data = {
            'like' : True
        }
    return JsonResponse(data)