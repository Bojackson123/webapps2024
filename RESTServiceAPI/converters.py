from decimal import Decimal

class DecimalConverter:
    regex = '[0-9]+(\.[0-9]+)?'

    def to_python(self, value):
        return Decimal(value)

    def to_url(self, value):
        return str(value)