from rest_framework import serializers
# from .models import Member, Meter, Reading, Invoice
from .models import *
from.serializers import *

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ['id', 'meter', 'member_number']

    def create(self, validated_data):
        member = Member.objects.create(**validated_data)
        member.member_number = member.generate_member_number()
        member.save()
        return member
    


class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = '__all__'

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = '__all__'

class ReadingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        exclude = ['read_sequence', 'tariff_rate']

    def create(self, validated_data):
        meter = validated_data['meter']
        meter_tariff_rate = meter.tariff_rate if meter.tariff_rate else 150

        reading = Reading.objects.create(
            meter=validated_data['meter'],
            reading_date=validated_data['reading_date'],
            meter_reading=validated_data['meter_reading'],
            tariff_rate=meter_tariff_rate,
            status=validated_data.get('status', 0),
            date_inserted=validated_data.get('date_inserted'),
        )
        return reading


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        exclude = ['tarrif_rate']

