from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import   TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from .forms import LoginForm
from products.models import Product

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.all()
        
        context['products'] = products
        return context 


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return super(LoginView, self).form_invalid(form)


@login_required
def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('home'))