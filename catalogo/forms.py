from django import forms
from .models import Producto  # <— ajusta si tu modelo se llama distinto

class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"  # o ['name','price','stock','image',...]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
