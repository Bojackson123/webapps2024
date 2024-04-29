from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import CurrencyConversionSerializer
import requests


class ChangeCurrencyView(GenericAPIView):
    serializer_class = CurrencyConversionSerializer

    def get(self, request, currency1, currency2, amount_of_currency1):
        if currency1 and currency2 and amount_of_currency1:
            try:
                response = requests.get(f'https://v6.exchangerate-api.com/v6/0602661a0c446b9578336d0c/pair/'
                                        f'{currency1}/{currency2}/{amount_of_currency1}')
                response.raise_for_status()
                data = response.json()
                exchange_rate = data['conversion_rate']
                print(exchange_rate)
                converted_amount = data['conversion_result']
                print(converted_amount)
                conversion_data = {
                    "exchange_rate": exchange_rate,
                    "converted_amount": round(converted_amount, 2)
                }
                serializer = self.get_serializer(data=conversion_data)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data)
            except requests.RequestException as e:
                print(f"Error fetching exchange rates: {e}")
                return Response({"error": "Error fetching data, please try later or change values."}, status=503)
            except KeyError:
                return Response({"error": "Currency is not supported by API."}, 422)
        return Response({"error": "Invalid currency conversion request."}, status=400)
