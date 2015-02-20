from django import forms


class AgencyData(forms.Form):

    public_liaison_email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
