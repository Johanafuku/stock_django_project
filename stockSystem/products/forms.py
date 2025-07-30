from django import forms
from .models import Product, Supplier, ProductSupplier

class ProductWithSuppliersForm(forms.ModelForm):
    suppliers = forms.ModelMultipleChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Proveedores'
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'suppliers']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'country']
        labels = {
            'name': 'Nombre del proveedor',
            'country': 'País de origen',
        }


class TransferStockForm(forms.Form):
    cantidad = forms.IntegerField(label="Cantidad a transferir", min_value=1)


class AddStockForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Product.objects.all(), label="Producto")
    proveedor = forms.ModelChoiceField(queryset=Supplier.objects.none(), label="Proveedor")
    cantidad = forms.IntegerField(min_value=1, label="Cantidad a agregar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estamos recibiendo datos del usuario (POST o GET con datos)
        if self.data.get('producto'):
            try:
                producto_id = int(self.data.get('producto'))
                self.fields['proveedor'].queryset = Supplier.objects.filter(
                    id__in=ProductSupplier.objects.filter(product_id=producto_id).values_list('supplier_id', flat=True)
                )
            except (ValueError, TypeError):
                self.fields['proveedor'].queryset = Supplier.objects.none()
        elif self.initial.get('producto'):
            producto_id = self.initial.get('producto').id
            self.fields['proveedor'].queryset = Supplier.objects.filter(
                id__in=ProductSupplier.objects.filter(product_id=producto_id).values_list('supplier_id', flat=True)
            )