from django.urls import path
from .views import itemView, itemCrudView

urlpatterns = [
    path('',itemView,name="items"),
    path('crud/<int:pk>/',itemCrudView,name="items-crud")
]