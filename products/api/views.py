from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import permissions

from ..models import Products
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

class ProductAPIList(ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter] # ('name',)
    filter_fields = ['name']
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]


class ProductAPICreate(CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductAPIRetrieve(RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]


"""
create search button V
specify the current user in when creating a post V
add user field to table V
IsAdminOrReadOnly V
IsOwnerOrReadOnly
"""


"""
views.py
class PurchaseList(generics.ListAPIView):
    #This view should return a list of all the purchases for the currently authenticated user.
    def get_queryset(self):
        user = self.request.user
        return Purchase.objects.filter(purchaser=user)

        
models.py
class Purchase(models.Model):
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
"""