from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Item(models.Model):

    bike = 'bi'
    car = 'ca'
    electronic = 'el'
    furniture = 'fu'
    housing = 'ho'
    phone = 'ph'

    category_list = [
        (bike, 'BIKE'),
        (car, 'CAR'),
        (electronic, 'ELECTRONIC'),
        (furniture, 'FURNITURE'),
        (housing, 'HOUSING'),
        (phone, 'PHONE'),   
    ]

    category = models.CharField(max_length=2, choices=category_list, default='bike')
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='item_image')
    listing_price = models.IntegerField()
    name = models.CharField(max_length=100)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_id = models.TextField()

    def __str__(self):
        return self.author.username

    def last_10_messages(room_id):
        
        messages = Message.objects.filter(room_id=room_id).order_by('-timestamp')[:10]
        if messages:
            return messages
