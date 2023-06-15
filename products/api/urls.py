from django.urls import path

from .views import ProductAPICreate, ProductAPIList, ProductAPIRetrieve

urlpatterns = [
    path('list/', ProductAPIList.as_view()),
    path('create/', ProductAPICreate.as_view()),
    path('<int:pk>/', ProductAPIRetrieve.as_view()),
]