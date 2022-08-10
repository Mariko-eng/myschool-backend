from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CategorySerializer,ItemSerializer
from .models import Category, Item

class CategoryView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

categoryView = CategoryView.as_view()

class ItemView(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

itemView = ItemView.as_view()

class ItemCrudView(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

itemCrudView = ItemCrudView.as_view()