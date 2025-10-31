from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "class": "input"}),
            "precio": forms.NumberInput(attrs={"step": "0.01", "class": "input"}),
            "stock": forms.NumberInput(attrs={"min": 0, "class": "input"}),
        }

    def clean_imagen(self):
        """
        Si el usuario marcó 'limpiar' y además subió un archivo nuevo,
        preferimos el archivo nuevo y NO mostramos el error.
        """
        # este campo puede traer varias cosas en request.FILES / request.POST
        uploaded_file = self.files.get("imagen")
        clear_checkbox = self.data.get(self.add_prefix("imagen-clear"))

        # caso feo de Django: marcó limpiar y subió archivo -> nos quedamos con el archivo
        if uploaded_file and clear_checkbox:
            return uploaded_file

        # en los demás casos dejamos que Django haga lo normal
        return self.cleaned_data.get("imagen")