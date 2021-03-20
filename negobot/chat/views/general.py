from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

def index(request):

    return render(request, 'index.html', {})

def logout(request):

    auth.logout(request)
    return redirect('/chat')

def login(request):

    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            return render(request, 'home.html', {'username': username})
        else:
            messages.info(request, 'invalid credentials')
            return redirect('index')

    else:
        return render(request,'index.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email id already registered')
                return redirect('register')
            else:   
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request, 'Login to continue')
                return redirect('index')

        else:
            messages.info(request,'password not matching..')    
            return redirect('register')
        
    else:
        return render(request,'register.html')

def account_details(request):

    username = request.session.get('username')
    account = User.objects.get(username=username)
    return render(request, 'account/account_details.html', {'account': account, 'username': username})

def room(request, room_id):
    
    return render(request, 'chat/room.html', {
        'room_id': room_id,
        'username': request.session.get('username'),
    })

