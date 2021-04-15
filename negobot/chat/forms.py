from django import forms 
from .models import Item 

class ItemForm(forms.ModelForm): 

	class Meta: 
		model = Item
		fields = ('name', 'category', 'description', 'listing_price')
		labels = {
		"name": "Name your product",
        "category": "Select a category for your product",
		"description": "Give a description of your product",
		"listing_price": "Enter your product's selling / listing price",
    	}
