from django.db import models
from django.conf import settings


class Transaction(models.Model):
    CURRENCY_CHOICES = [
        ("GBP", "Pound Sterling"),
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
    ]
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency_sign = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")
    is_request = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_convert = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} - Amount: {self.amount}"
