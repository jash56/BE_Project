from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from ..models import Item
from ..forms import ItemForm

class ItemCreateView(CreateView):
    model = Item
    template_name = 'item/item_create_update.html'
    form_class = ItemForm

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            seller = self.request.session.get('username')
            item.seller = User.objects.get(username=seller)
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
        return context

class ItemUpdateView(UpdateView):

    model = Item
    template_name = 'item/item_create_update.html'
    form_class = ItemForm

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.id = self.kwargs['pk']
            seller = self.request.session.get('username')
            item.seller = User.objects.get(username=seller)
            item.save()
            return redirect('my-item-list')
        return render(request, 'item/item_create_update.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('username')
        return context

def item_delete(request, pk):

    Item.objects.get(id=pk).delete()
    return redirect('my-item-list')