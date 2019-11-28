from rest_framework import serializers
from .models import Delivery, Parcel


class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'


class ParcelSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = (
            "length",
            "width",
            "height",
            "weight",
            "real_length",
            "real_width",
            "real_height",
            "real_weight",
            "total_weight",
            "over_weight",
        )


class DeliverySerializer(serializers.ModelSerializer):
    parcel = ParcelSerializer()
    def create(self, validated_data):

        instance = Delivery.objects.create(**validated_data)

        parcel = validated_data['parcel']
        parcel['delivery'] = instance.id
        parcel_created = ParcelSerializer(data=parcel)
        parcel_created.is_valid(raise_exception=True)
        parcel_created = parcel_created.save()
        return instance

    class Meta:
        model = Delivery

        fields = (
            "id",
            "tracking_number",
            "carrier",
            "parcel",
        )


class DeliveryReadSerializer(serializers.ModelSerializer):
    parcel = serializers.SerializerMethodField()

    def get_parcel(self, obj):
        parcel_obj = Parcel.objects.filter(delivery_id=obj.id).first()
        parcel = ParcelSerializerRead(parcel_obj).data
        return parcel

    class Meta:
        model = Delivery

        fields = (
            "id",
            "tracking_number",
            "carrier",
            "parcel",
        )
