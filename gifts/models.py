from django.db import models
from django.contrib.auth.models import User

import secrets
import string

# Create your models here.
class Gift(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='gifts')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    provider = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def buy(self, user):
        # Check if user has enough credit
        if user.profile.credit < self.price:
            return False, 'Not enough credit, contribute more to the comunitty to earn more credit.'

        if self.stock > 0:
            self.stock -= 1
            self.save()

            user.profile.credit -= float(self.price)
            user.profile.save()

            order = GiftOrder.objects.create(gift=self, user=user)
            return True, "you'll receive a message on your phone number containing your gift details, please note that this could take a few minutes."
        else:
            return False, 'Gift out of stock'


class GiftOrder(models.Model):
    state_choices = [
        ('pending', 'pending'),
        ('rejected', 'rejected'),
        ('confirmed', 'confirmed')
    ]
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=state_choices, default='pending')

    def __str__(self):
        return f'Order for {self.gift.name}'

    def confirm_and_generate_code(self):
        if self.state == 'pending':
            self.state = 'confirmed'
            self.save()
            code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9))  # Generate a random 9-character alphanumeric code
            gift_code = GiftCode.objects.create(code=code, order=self)
            return True, 'Order confirmed and gift code generated', code
        else:
            print(self.state)
            return False, 'Order is not pending', None


class GiftCode(models.Model):
    order = models.ForeignKey(GiftOrder, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code