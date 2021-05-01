from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth # authenticate whether user exits in auth_user table or not.
from django.contrib.auth.decorators import login_required # restrict us to acces a particular view
from django.contrib import messages
from django.db import IntegrityError

# importing form classes
from django.contrib.auth.forms import UserCreationForm
from users.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, Login

# importing friends and Profile from users
from users.models import friends, Profile

# handle login and verification data and rendering 
def login(request):
    if request.method == 'POST':
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mobile = form.cleaned_data.get('mobile')
            # authenticate whether the logged in user is valid or not
            user = auth.authenticate(username=username, password=password)

            if user is not None: 
                if user.profile.mobile == mobile: # validating mobile number
                    auth.login(request, user)
                    return redirect('posts-home')
                
                else:
                    messages.info(request, 'mobile number doesnot exist')
                    return redirect('login')

            else:
                messages.info(request, 'Incorrect Credentials')
                return redirect('login')


    else: # Executed, if the request is GET
        form = Login()
        return render(request, 'users/login.html', {'form':form})


# handles user registration data and rendering 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                mobile = request.POST['mobile']
                user = User.objects.get(username=username)
                mobile_user = Profile.objects.get(user=user)
                mobile_user.mobile=mobile
                mobile_user.save()
                messages.success(request, f'Your account has been created. You are now able to login {username}!')
                return redirect('login')
        except IntegrityError as e: # handle integrity error
            if 'UNIQUE constraint' in str(e.args):
                messages.info(request, 'Mobile number already exist!')
                return redirect('register')


    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

# handles profile data and rendering 
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                  request.FILES,
                                  instance=request.user.profile)


        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    count = friends.objects.filter(user_friend=request.user)
    total = 0
    for c in count:
        total = total + 1
    
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'total' : total,
    }

    return render(request, 'users/profile.html', context)


# show all friends in 'make friends' section 
def showAllUser(request):
    all_user = User.objects.all()
    to_check_friend = friends.objects.filter(user_friend=request.user)
    request_user = request.user
    friend = []
    for x in to_check_friend:
        friend.append(x.conn_user)
    
    context = {
        'all_user' : all_user,
        'friend' : friend,
        'request_user' : request_user,
    }
    return render(request, 'posts/alluser.html', context)


# To add a friend 
def added_friend(request):
    usrname = request.POST.get('data')
    t = friends(conn_user=usrname)
    t.save()
    t.user_friend.add(request.user)
    messages.info(request, 'You are now friends')
    return redirect('alluser')


# Show all friends of current user
def show_friends(request):
    connected_friends = friends.objects.filter(user_friend=request.user.id)
    friends_list = []
    for x in connected_friends:
        friends_list.append(x.conn_user)

    all_user = User.objects.all()   # took all_user from User table 
    context = {
        'friends_list' : friends_list,
        'all_user' : all_user,
    }
    return render(request, 'posts/show_user.html', context)