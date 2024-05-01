from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import CurrencyConversionSerializer


class ChangeCurrencyView(GenericAPIView):
    # initialize serializer
    serializer_class = CurrencyConversionSerializer
    # create exchange rates dict with GBP being the central currency for exchanges
    # this avoids circular conversion errors adding up.
    exchange_rates = {
        ('GBP', 'USD'): 1.25,
        ('USD', 'GBP'): 0.8,
        ('GBP', 'EUR'): 1.17,
        ('EUR', 'GBP'): 1 / 1.17,
        ('USD', 'EUR'): (0.8 * 1.17),
        ('EUR', 'USD'): 1 / (0.8 * 1.17),
        ('USD', 'USD'): 1.00,
        ('GBP', 'GBP'): 1.00,
        ('EUR', 'EUR'): 1.00,
    }

    # get method for currency conversion
    def get(self, request, currency1, currency2, amount_of_currency1):
        if currency1 and currency2 and amount_of_currency1:
            try:
                amount_in_gbp = float(amount_of_currency1)
                if currency1 != 'GBP':
                    amount_in_gbp *= self.exchange_rates[(currency1, 'GBP')]

                converted_amount = amount_in_gbp
                if currency2 != 'GBP':
                    converted_amount *= self.exchange_rates[('GBP', currency2)]

                conversion_data = {
                    "exchange_rate": converted_amount / float(amount_of_currency1),
                    "converted_amount": converted_amount
                }
                serializer = self.get_serializer(data=conversion_data)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data)
            except Exception as e:
                print(f"Error fetching converted currency: {e}")
                return Response({"error": "Error fetching data, please try later."}, status=503)
        return Response({"error": "Invalid currency conversion request."}, status=400)
