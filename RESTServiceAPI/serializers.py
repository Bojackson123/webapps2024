from rest_framework import serializers


class CurrencyConversionSerializer(serializers.Serializer):
    converted_amount = serializers.DecimalField(max_digits=30, decimal_places=20)
