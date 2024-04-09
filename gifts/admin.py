from django.contrib import admin
from .models import Gift, GiftOrder, GiftCode   

# Register your models here.
admin.site.register(Gift)
admin.site.register(GiftOrder)
admin.site.register(GiftCode)