from rest_framework import serializers
from .models import Gift, GiftOrder, GiftCode
from django.contrib.auth.models import User

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'

class GiftOrderSerializer(serializers.ModelSerializer):
    gift = GiftSerializer()
    user = serializers.SerializerMethodField()

    class Meta:
        model = GiftOrder
        fields = ['id', 'gift', 'user', 'created_at', 'state']
    
    def get_user(self, obj):
        user = User.objects.get(id=obj.user.id)
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile': {
                'role': user.profile.role,
                'verified': user.profile.verified,
                'school': user.profile.school.libar if user.profile.school else None,
                'grade': user.profile.grade.libar if user.profile.grade else None,
                'credit': user.profile.credit,
                'finished': user.profile.finished,
                'lat': user.profile.lat,
                'lng': user.profile.lng,
                'picture': user.profile.picture.url,
            }
        }

class GiftCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCode
        fields = ['id', 'code', 'order', 'used']