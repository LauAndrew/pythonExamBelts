from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    if request.method == "POST":
        errors = User.objects.validate(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/main')
        else:
            found_users = User.objects.filter(email=request.POST['email'])
            if found_users.count() > 0:
                messages.error(request, "Email already taken", extra_tags="email")
                return redirect('/main')
            else:
                hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                created_user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hashed_pw)
                request.session['id'] = User.objects.get(email=request.POST['email']).id
                return redirect('/dashboard')
    return render(request, 'friends_app/index.html')

def login(request):
    found_users = User.objects.filter(email=request.POST['email'])
    if found_users.count() > 0:
        found_user = found_users.first()
        if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
            request.session['id'] = User.objects.get(email=request.POST['email']).id
            return redirect('/dashboard')
        else:
            messages.error(request, "Login Failed, incorrect password", extra_tags="password")
            return redirect('/')
    else:
        messages.error(request, "Login Failed, username is not registered", extra_tags="username")
        return redirect('/')

def logout(request):
    request.session['id'] = 0
    return redirect('/')

                                # ++=============Login/Registration DONE HERE=============++

def dashboard(request):
    myself = User.objects.get(id=request.session['id'])
    try:
        users = User.objects.all()
        others = []
        for other_user in users:
            if (other_user.id != request.session['id']):
                others.append(other_user)
    except:
        users = None

    try:
        friends = Friend.objects.filter(user_friend=myself)
        a_friends = []
        for each_friend in friends:
            a_friends.append(each_friend.second_friend)
        u_others = []
        for other_user in others:
            if (other_user not in a_friends):
                u_others.append(other_user)
    except:
        friends = None

    context = {
        'me' : myself,
        'users' : u_others,
        'friends' : a_friends
    }
    return render(request, 'friends_app/dashboard.html', context)

def add_friend(request, id):
    User.objects.addFriend(request.session['id'], id)
    return redirect('/dashboard')

def remove_friend(request, id):
    User.objects.removeFriend(request.session['id'], id)
    return redirect('/dashboard')

def profile(request, id):
    user_profile = User.objects.get(id=id)
    context = {
        'user' : user_profile
    }
    return render(request, 'friends_app/profile.html', context)