from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CurrencyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)
        self.fields['currency'].widget.attrs.update({
            'class': 'form-select',
        })

    class Meta:
        model = User
        fields = ['currency']
