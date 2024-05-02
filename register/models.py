from django.contrib.auth.models import AbstractUser
from django.db import models
import requests
from decimal import Decimal


class User(AbstractUser):
    CURRENCY_CHOICES = [
        ("GBP", "Pound Sterling"),
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
    ]

    balance = models.DecimalField(max_digits=30, decimal_places=10, default=1000.0000000000)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="GBP")

    CURRENCY_SIGNS = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
    }

    def get_currency_sign(self):
        return self.CURRENCY_SIGNS.get(self.currency, self.currency)

