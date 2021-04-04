from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

from ..models import Item, Message, TargetPrice

from mlmodel import get_reccomendation

def index(request):

    return render(request, 'index.html', {})

def logout(request):

    auth.logout(request)
    return redirect('/chat')

def home(request):

    return render(request, 'home.html', {'username':request.session.get('username')})

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
            messages.info(request, 'Invalid credentials')
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
            messages.info(request,'Password not matching..')    
            return redirect('register')
        
    else:
        return render(request,'register.html')

def account_details(request):

    username = request.session.get('username')
    account = User.objects.get(username=username)
    return render(request, 'account/account_details.html', {'account': account, 'username': username})

def room(request, room_id):

    reccomendation = "Click the 'Get reccomendation' button!"
    a = list()
    for i in room_id:
        try:
            a.append(int(i))
        except:
            break
    b = ''.join([str(elem) for elem in a])
    a = int(b)
    item = Item.objects.get(id=a)
    try:
        buyer_target = TargetPrice.objects.get(room_id=room_id).target_price
    except:
        buyer_target = 0

    if request.method == 'POST' and 'target_price' in request.POST:
        target_price = request.POST['target']
        try:
            target = TargetPrice.objects.get(room_id=room_id)
            target.target_price = target_price
            target.save()
        except:
            target = TargetPrice(target_price=target_price, room_id=room_id)
            target.save()
    elif request.method == 'POST' and 'reccomendation' in request.POST:
        message_list = Message.objects.filter(room_id=room_id)
        messages =  ' '.join([str(message.content) for message in message_list])        
        seller_target = item.listing_price
        reccomendation = get_reccomendation(messages, buyer_target, seller_target)

    return render(request, 'chat/room.html', {
        'buyer_target': buyer_target,
        'reccomendation': reccomendation,
        'item': item,
        'room_id': room_id,
        'username': request.session.get('username'),
    })



