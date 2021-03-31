from django.urls import path
from .views import general, item

urlpatterns = [
    path('', general.index, name='index'),
    path('logout', general.logout, name='logout'),
    path('login', general.login, name='login'),
    path('register', general.register, name='register'),
    path('home', general.home, name='home'),

    path('myAccount', general.account_details, name='my-account'),

    path('<str:room_id>/', general.room, name='room'),

    path('newItem', item.ItemCreateView.as_view(), name='new-item'),
    path('myItemList', item.MyItemListView.as_view(), name='my-item-list'),
    path('itemList', item.ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', item.ItemDetailView.as_view(), name='item-detail'),
    path('updateItem/<int:pk>/', item.ItemUpdateView.as_view(), name='update-item'),
    path('deleteItem/<int:pk>/', item.item_delete, name='delete-item'),

    path('listBuyers/<int:pk>/', item.buyer_list, name='list-buyers'),
]