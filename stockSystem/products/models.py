from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name='Nombre del producto')
    description = models.CharField(max_length=500, verbose_name='Detalle técnico')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Precio')
    stock = models.IntegerField(verbose_name='Stock total')
    minimum_stock = models.IntegerField(default=50,verbose_name='stock mínimo')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        
    @property
    def stock_minimo(self):
        return self.stock <= self.minimum_stock
    
    def __str__(self):
        return f"{self.name} registrado"
    
    @property
    def proveedores(self):
        return [ps.supplier for ps in self.productsuppliers.all()]
    

class Supplier(models.Model):
    name = models.CharField(max_length=300, verbose_name='Nombre del proveedor')
    country = models.CharField(max_length=200, verbose_name='País de origen')

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.name
    

class ProductSupplier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto', related_name="productsuppliers")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Proveedor')
    

    class Meta:
        verbose_name = 'Producto por proveedor'
        verbose_name_plural = 'Productos por proveedor'
        unique_together = ('product', 'supplier')  # Evita duplicaciones

    def __str__(self):
        return f"{self.product.name} de {self.supplier.name}"