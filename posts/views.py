from django.shortcuts import render, redirect, HttpResponse
from posts.models import Post
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.models import friends
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# show all post of current user and his friends in home page 
@login_required
def showPost(request):
    posts = Post.objects.all().order_by('-date_posted')
    connected_friends = friends.objects.filter(user_friend=request.user)
    friends_list = []
    for x in connected_friends:
        friends_list.append(x.conn_user)
    friends_list.append(request.user.username)
    context = {
        'posts' : posts,
        'friends_list' : friends_list,
    }
    return render(request, 'posts/home.html', context)


# Shows detail of each post
def PostDetailView(request, slug):
    q = Post.objects.filter(slug__iexact = slug)
    if q.exists():
        q = q.first() # row object 
        print(q) 

    else:
        return HttpResponse('<h1> Post Not Found </h1>')

    context = {
        'post' : q
    }

    return render(request, 'posts/post_detail.html', context)


# To create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'img']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user_post = self.request.user
        return super().form_valid(form)

# To update post 
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'img']

    def form_valid(self, form):
        form.instance.user_post = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user_post:
            return True
        return False

# To delete a post 
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user_post:
            return True
        return False


# To see details of each user in 'friends' or 'make friends' section
class UserDetailView(DetailView):
    model = User
    template_name = 'posts/user_detail.html'

    def get_context_data(self,*args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args,**kwargs)
        all_friends = friends.objects.filter(user_friend=self.object)
        fri_list = []
        for x in all_friends:
            fri_list.append(x.conn_user)

        context['fri_list'] = fri_list
        return context

# handles search functionality 
def search(request):
    query = request.GET['query']   
    all_user = User.objects.all()
    request_user = request.user
    to_check_friend = friends.objects.filter(user_friend=request.user)
    friend = []
    for x in to_check_friend:
        friend.append(x.conn_user)
        

    try: # executed if query = mobile number
        if type(int(query)) == int:
            mob_user = Profile.objects.get(mobile=query)
            context = {
                'username' : mob_user.user_mobile.username,
                'email' : mob_user.user_mobile.email,
                'mobile' : mob_user.user_mobile.mobile.mobile,
                'all_user' : all_user,
                'request_user' : request_user,
                'friend' : friend,
                'mob_user' : mob_user,
                'query' : query,
            }
            return render(request, 'posts/search.html', context) 

    except ValueError:
        x = True

    if x: # executed, if query is a username or emailID
        found = User.objects.filter(Q(username=query) | Q(email=query))
        context = {
            'found' : found,
            'all_user' : all_user,
            'request_user' : request_user,
            'to_check_friend' : to_check_friend,
            'friend' : friend,
            'query' : query,
        }
        return render(request, 'posts/search.html', context)



