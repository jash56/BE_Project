from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from ..models import Item, Message
from ..forms import ItemForm

import pyrebase
import os

config = {
    "apiKey": "AIzaSyDj9DPTgoKXN1mc6yn6oLvuVif1GGcV1RA",
    "authDomain": "negobot-dca88.firebaseapp.com",
    "projectId": "negobot-dca88",
    "storageBucket": "negobot-dca88.appspot.com",
    "messagingSenderId": "309578681717",
    "appId": "1:309578681717:web:4c6aeabd4bb571a28d573c",
    "measurementId": "G-4DV29PEF44",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

class ItemCreateView(CreateView):
    model = Item
    template_name = 'item/item_create_update.html'
    form_class = ItemForm

    def post(self, request, *args, **kwargs):
        form = ItemForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            seller = self.request.session.get('username')
            item.seller = User.objects.get(username=seller)
            item.image_url = ''
            item.save()
            storage.child(seller + '/' + str(item.id)).put(request.FILES['image'])
            item.image_url = storage.child(seller + '/' + str(item.id)).get_url(None)
            item.save()
            return redirect('my-item-list')
        return render(request, 'item/item_create_update.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('username')
        return context
    
class ItemListView(ListView):

    model = Item
    paginate_by = 50
    ordering = 'name'
    template_name = 'item/item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('username')
        context['text'] = 'Be a buyer. What would you like to buy today?'
        return context

    def get_queryset(self):
        lst = list()
        current_user = self.request.session.get('username')
        current_user = User.objects.get(username=current_user)
        current_user_list = Item.objects.filter(seller=current_user)
        all_user_list = Item.objects.all()
        for item in all_user_list:
            if item not in current_user_list:
                lst.append(item)
        return lst

class MyItemListView(ListView):

    model = Item
    paginate_by = 50
    ordering = 'name'
    template_name = 'item/item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('username')
        context['text'] = "Be a seller. Let's take a look at what you have to sell!"
        context['add_item'] = True
        return context

    def get_queryset(self):
        current_user = self.request.session.get('username')
        current_user = User.objects.get(username=current_user)
        return Item.objects.filter(seller=current_user)


class ItemDetailView(DetailView):

    model = Item
    template_name = 'item/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('username')
        if self.request.method == "GET":
            context['image_url'] =  storage.child(context['username'] + '/' + str(self.kwargs['pk'])).get_url(None)
        return context

class ItemUpdateView(UpdateView):

    model = Item
    template_name = 'item/item_create_update.html'
    form_class = ItemForm

    def post(self, request, *args, **kwargs):
        form = ItemForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.id = self.kwargs['pk']
            seller = self.request.session.get('username')
            item.seller = User.objects.get(username=seller)
            image = request.FILES.get('image', False)
            if image is False:
                item.image_url = Item.objects.get(id = self.kwargs['pk']).image_url
            else:
                storage.child(seller + '/' + str(item.id)).put(image)
                item.image_url = storage.child(seller + '/' + str(item.id)).get_url(None)
            item.save()
            return redirect('my-item-list')
        return render(request, 'item/item_create_update.html', {'form': form})

    def get_context_data(self, **kwargs):
        item_id = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('username')
        if self.request.method == "GET":
            context['image_url'] =  storage.child(context['username'] + '/' + str(item_id)).get_url(None)
        return context

def item_delete(request, pk):

    item = Item.objects.get(id=pk)
    #storage.refFromUrl(item.image_url).delete()
    item.delete()
    return redirect('my-item-list')

def buyer_list(request, pk):

    item = Item.objects.get(id=pk)
    username = request.session.get('username')
    messages = Message.objects.all()
    pk = str(pk)
    pk_length = len(pk)
    buyers = list()
    for message in messages:

        room = message.room_id
        item_id = room[:pk_length]
        buyer_id = room[pk_length:]
    
        if pk == item_id:
            if len(buyer_id) > 0:
                buyers.append(buyer_id)

    return render(request, 'item/item_buyer_list.html', {'buyers': set(buyers), 'username': username, 'item': item,})