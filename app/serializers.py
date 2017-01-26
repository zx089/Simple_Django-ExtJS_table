
from rest_framework import serializers
from app.models import Parcel


class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('id', 'first_name', 'last_name', 'sender_name', 'city', 'delivery_status')

        first_name = serializers.CharField(max_length=255)
        last_name = serializers.CharField(max_length=255)
        sender_name = serializers.CharField(max_length=255)
        city = serializers.CharField(max_length=255)
        delivery_status = serializers.CharField(max_length=255)


        def create(self, validated_data):
            return Parcel.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.sender_name = validated_data.get('sender_name', instance.sender_name)
            instance.city = validated_data.get('city', instance.city)
            instance.delivery_status = validated_data.get('delivery_status', instance.delivery_status)
            instance.save()
            return instance

