from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .models import Products, Basket, ProductCategories
from .forms import RegisterForm, LoginForm, ProfileForm

##################################################################################
# def index(request):
#     categories = ProductCategories.objects.all()
#     products = Products.objects.all()
#     return render(request, 'products/index.html', {"products": products, 'categories': categories})

class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['categories'] = ProductCategories.objects.all()
        context['products'] = Products.objects.all()
        return context
##################################################################################

# def show_product(request, product_id):
#     product = Products.objects.get(id=product_id)
#     return render(request, 'products/product.html', {'product': product})

class ProductDetailView(DetailView):
    model = Products # products_detail.html
    template_name = 'products/product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

##################################################################################
# def show_category(request, cat_id):
#     categories = ProductCategories.objects.all()
#     products = Products.objects.filter(category_id=cat_id)
#     return render(request, 'products/index.html', {'products': products, 'categories': categories})
class CategoryListView(ListView):
    model = Products # products_list.html
    template_name = 'products/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Products.objects.filter(category_id=self.kwargs['cat_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategories.objects.all()
        return context

##################################################################################
# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             messages.success(request, 'Account created successfully!')
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)

##################################################################################
# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request=request, username=username, password=password)
#             if user is not None:
#                 login(request=request, user=user)
#                 return redirect('index')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/products/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request=self.request, username=username, password=password)
        if user is not None:
            login(request=self.request, user=user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)
        
##################################################################################
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

##################################################################################
# @login_required
# def profile_view(request):
#     if request.method == 'POST':
#         form = ProfileForm(instance=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#         else:
#             print(form.errors)
#     else:
#         form = ProfileForm(instance=request.user)

#     baskets = Basket.objects.filter(user=request.user)

#     return render(request, 'profile.html', {'form': form, 'baskets': baskets})

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = '/profile/'

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        baskets = Basket.objects.filter(user=self.request.user)
        context = self.get_context_data(form=form, baskets=baskets)
        return self.render_to_response(context)

##################################################################################
@login_required
def basket_add(request, product_id):
    product = Products.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
