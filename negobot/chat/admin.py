from django.contrib import admin
from .models import Message, Item

# Register your models here.
admin.site.register(Message)
admin.site.register(Item)