from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Gift, GiftOrder, GiftCode
from .serializers import GiftSerializer, GiftOrderSerializer, GiftCodeSerializer
from . import utils

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):

    # Get all orders with custom ordering and ordered by created_at newest first
    orders = GiftOrder.objects.filter(user=request.user).order_by('-state', '-created_at')
    serializer = GiftOrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gift_list(request):
    gifts = Gift.objects.filter(available=True)
    serializer = GiftSerializer(gifts, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_gift(request):
    gift_id = request.data['gift_id']
    gift = Gift.objects.get(id=gift_id)
    success, message = gift.buy(request.user)
    if success:
        return Response({'message': message})
    else:
        return Response({'message': message}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_orders(request):
    orders = GiftOrder.objects.filter(state='Pending', user=request.user)
    serializer = GiftOrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_order(request):
    order_id = request.data['order_id']
    order = GiftOrder.objects.get(id=order_id)
    success, message, code = order.confirm_and_generate_code()

    if success:
        utils.send_gift_code(order.user.username, code, order.user.first_name,order.gift.provider)
        return Response({'message': message, 'code': code})
    else:
        return Response({'message': message}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_gift_codes(request):
    gift_codes = GiftCode.objects.filter(order__user=request.user)
    serializer = GiftCodeSerializer(gift_codes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_gift(request):
    data = request.data.copy()
    data['available'] = 'True'

    serializer = GiftSerializer(data=data)
    
    if serializer.is_valid():
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=400)


# -----------------------------------to be added to retailer actor
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def redeem_code(request):
#     code = request.data['code']
#     gift_code = GiftCode.objects.get(code=code)
#     if gift_code.used:
#         return Response({'message': 'Code already used'}, status=400)
#     gift_code.used = True
#     gift_code.save()
#     gift_order = gift_code.order
#     gift_order.state = 'Completed'
#     gift_order.save()
#     return Response({'message': 'Gift redeemed successfully'})