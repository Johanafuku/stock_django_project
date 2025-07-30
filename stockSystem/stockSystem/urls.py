
from django.contrib import admin
from django.urls import path
from .views import HomeView, LoginView, logout_view
from products.views import ProductCreateWithSuppliersView, SupplierCreateView, ProductListView, TransferStockView, AgregarStockView
from django.conf.urls.static import static  
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('productos/agregar/',ProductCreateWithSuppliersView.as_view(), name='create_product'),
    path('productos/lista/', ProductListView.as_view(), name='list_product'),
    path('productos/transferir/<int:pk>/', TransferStockView.as_view(), name='transfer_stock'),
    path('proveedores/agregar/',SupplierCreateView.as_view(), name='create_provider'),
    path('productos/agregar_stock/', AgregarStockView.as_view(), name='add_stock'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
