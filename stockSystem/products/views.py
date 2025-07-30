from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import ProductWithSuppliersForm, SupplierForm, TransferStockForm, AddStockForm
from .models import Product, Supplier, ProductSupplier
from django.views.generic import  CreateView, ListView, FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductCreateWithSuppliersView(CreateView):
    model = Product
    form_class = ProductWithSuppliersForm
    template_name = 'products/create_product.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Guardamos primero el producto
        response = super().form_valid(form)
        producto = self.object  

        # Creamos la relación con los proveedores seleccionados
        for proveedor in form.cleaned_data['suppliers']:
            ProductSupplier.objects.create(
                product=producto,
                supplier=proveedor,
                
            )
            messages.success(self.request, 'Producto creado con éxito')
        return response


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'products/create_provider.html'
    success_url = reverse_lazy('home')  


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
class TransferStockView(FormView):
    template_name = 'products/transfer_stock.html'
    form_class = TransferStockForm

    def dispatch(self, request, *args, **kwargs):
        self.producto = get_object_or_404(Product, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producto'] = self.producto
        context['alerta'] = (
        "⚠️ Alerta: Stock por debajo del mínimo"
        if self.producto.stock_minimo else None
        )
        return context

    def form_valid(self, form):
        cantidad = form.cleaned_data['cantidad']
        if self.producto.stock >= cantidad:
            self.producto.stock -= cantidad
            self.producto.save()
            return super().form_valid(form)
        else:
            form.add_error('cantidad', 'No hay suficiente stock disponible.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('list_product')
    

@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
class AgregarStockView(FormView):
    template_name = 'products/add_stock.html'
    form_class = AddStockForm
    success_url = reverse_lazy('list_product')

    def form_valid(self, form):
        producto = form.cleaned_data['producto']
        cantidad = form.cleaned_data['cantidad']

        producto.stock += cantidad
        producto.save()

        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs['data'] = self.request.GET
        return kwargs
    
