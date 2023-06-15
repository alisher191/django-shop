from django.urls import path, include

from .views import IndexView, basket_add, basket_remove, CategoryListView, ProductDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('basket/add/<int:product_id>', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>', basket_remove, name='basket_remove'),
    path('category/<int:cat_id>/', CategoryListView.as_view(), name='category'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product'),
]
