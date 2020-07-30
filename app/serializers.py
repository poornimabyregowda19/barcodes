from rest_framework import serializers
from app.models import Barcode

class BarcodeSerializer(serializers.ModelSerializer):
    feature = serializers.SlugRelatedField(
        read_only=True,
        slug_field='uid'
    )
    class Meta:
        model = Barcode
        fields = ['serial_number', 'feature','num_modules_horizontal', 'num_modules_vertical' ]



