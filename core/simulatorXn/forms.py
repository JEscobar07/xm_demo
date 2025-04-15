from django import forms
from .models import Frontera

class FronteraForm(forms.ModelForm):
    """
    Form used to register Frontera data from the user.
    """
    class Meta:
        model = Frontera
        fields = '__all__'
