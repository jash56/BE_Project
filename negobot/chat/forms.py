from django import forms 
from .models import Item 

class ItemForm(forms.ModelForm): 

	class Meta: 
		model = Item
		fields = ('category', 'description', 'listing_price', 'name')
		labels = {
        "category": "Select a category for your product",
		"description": "Give a description of your product",
		"listing_price": "Enter your product's selling / listing price",
		"name": "Name your product",
    }
