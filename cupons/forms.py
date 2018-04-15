from django import forms


class CuponApllyForm(forms.Form):
    code = forms.CharField(label='Код')
