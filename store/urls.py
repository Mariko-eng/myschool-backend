from django.urls import path
from .views import inwardStockView,outwardStockView
from .views import inwardStockCrudView,outwardStockCrudView
from .views import requisitionView,customRequistionView
from .views import requisitionCrudView,customRequistionCrudView

urlpatterns = [
    path('inward/',inwardStockView,name="inward"),
    path('inward-crud/<int:pk>/',inwardStockCrudView,name="inward-crud"),
    path('outward/',outwardStockView,name="outward"),
    path('outward-crud/<int:pk>/',outwardStockCrudView,name="outward-crud"),
    path('requisit/',requisitionView,name="requisit"),
    path('requisit-crud/<int:pk>/',requisitionCrudView,name="requisit-crud"),
    path('custom-requisit/',customRequistionView,name="custom-requisit"),
    path('custom-requisit-crud/<int:pk>/',customRequistionCrudView,name="custom-equisit-crud"),

]