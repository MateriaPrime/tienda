from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # 👇 aquí va stock también
        fields = ["nombre", "descripcion", "precio", "stock", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "precio": forms.NumberInput(attrs={"step": "0.01", "class": "input"}),
            "stock": forms.NumberInput(attrs={"min": 0, "class": "input"}),
            # imagen: dejamos el widget por defecto
        }
