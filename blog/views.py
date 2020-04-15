from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from users.models import Profile
from blog.forms import ProfileViewForm

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(LoginRequiredMixin,ListView):
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

    def get_queryset(self):
        profile = Profile.objects.filter(user_id=self.request.user.id).get().connections.all()
        connections = []
        for connection in profile:
            connections.append(connection.user_id)
        connections.append(self.request.user.id)
        queryset = Post.objects.filter(author_id__in=connections)
        return queryset

class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name='blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self,**kwargs):
        context = super(UserPostListView,self).get_context_data(**kwargs)
        liked = {}
        for post in context['posts']:
            liked[post.id] = post.likes.filter(id=self.request.user.id).exists()
        context['liked'] = liked
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        if self.request.user.id != user.id:
            res = self.request.user.profile.connections.filter(id=user.id).exists()
            if res:
                context['following'] = 1
            else:
                context['following'] = 0
        else:
            context['following'] = -1
        context['user_data'] = user
        profile = ProfileViewForm(instance=user.profile)
        context['profile_form'] = profile
        return context

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked = context['post'].likes.filter(id=self.request.user.id).exists()
        context['liked'] = liked
        return context

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

def connections(request):
    connections = request.user.profile.connections.all()
    print(connections)
    context = {
        'connections' : connections
    }
    return render(request, 'blog/connections.html', context)

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

def get_users(request):
    users = request.GET.get('user', None)
    users = User.objects.filter(username__istartswith=users).values_list('username')
    user_list = []
    for user in users:
        user_list.append(user[0])
    data = {}
    data['users'] = user_list
    return JsonResponse(data)

def follow(request):
    user_id = request.GET.get('user_id', None)
    host_id = request.GET.get('host_id', None)
    host = User.objects.filter(id=host_id).get()
    connections = host.profile.connections.filter(id=user_id).exists()
    if(connections):
        user = host.profile.connections.filter(id=user_id).get()
        host.profile.connections.remove(user)
        data = {
            'follow' : False
        }
    else:
        user = User.objects.filter(id=user_id).get()
        host.profile.connections.add(user.profile)
        data = {
            'follow' : True
        }
    return JsonResponse(data)