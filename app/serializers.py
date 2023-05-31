from rest_framework import serializers
from .models import Member, Meter, Reading, Invoice

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = '__all__'

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
