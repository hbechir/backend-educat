from django.urls import path
from . import views

urlpatterns = [
    path('', views.gift_list, name='gift_list'),
    path('buy-gift/', views.buy_gift, name='buy_gift'),
    path('pending-orders/', views.get_pending_orders, name='get_pending_orders'),
    path('get-all-orders/', views.get_all_orders, name='get_all_orders'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('gift-codes/', views.get_user_gift_codes, name='get_user_gift_codes'),
    path('add-gift/', views.add_gift, name='add_gift'),
    # path('redeem-code/', views.redeem_code, name='redeem_code'),  # Uncomment this line when you're ready to add this endpoint
]