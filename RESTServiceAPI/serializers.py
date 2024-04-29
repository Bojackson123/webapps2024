from rest_framework import serializers


class CurrencyConversionSerializer(serializers.Serializer):
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=4)
    converted_amount = serializers.DecimalField(max_digits=30, decimal_places=2)
