from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import InwardStockSerializer, OutwardStockSerializer
from .models import InwardStock, OutwardStock
from .serializers import RequisitionSerializer, CustomRequistionSerializer
from .models import Requisition,CustomRequisition

class InwardStockView(ListCreateAPIView):
    queryset = InwardStock.objects.all()
    serializer_class = InwardStockSerializer

inwardStockView = InwardStockView.as_view()

class InwardStockCrudView(RetrieveUpdateDestroyAPIView):
    queryset = InwardStock.objects.all()
    serializer_class = InwardStockSerializer

inwardStockCrudView = InwardStockCrudView.as_view()

class OutwardStockView(ListCreateAPIView):
    queryset = OutwardStock.objects.all()
    serializer_class = OutwardStockSerializer

outwardStockView = OutwardStockView.as_view()

class OutwardStockCrudView(RetrieveUpdateDestroyAPIView):
    queryset = OutwardStock.objects.all()
    serializer_class = OutwardStockSerializer

outwardStockCrudView = OutwardStockCrudView.as_view()

class RequisitionView(ListCreateAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer

requisitionView = RequisitionView.as_view()

class RequisitionCrudView(RetrieveUpdateDestroyAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer

requisitionCrudView = RequisitionCrudView.as_view()

class CustomRequistionView(ListCreateAPIView):
    queryset = CustomRequisition.objects.all()
    serializer_class = CustomRequistionSerializer

customRequistionView = CustomRequistionView.as_view()

class CustomRequistionCrudView(RetrieveUpdateDestroyAPIView):
    queryset = CustomRequisition.objects.all()
    serializer_class = CustomRequistionSerializer

customRequistionCrudView = CustomRequistionCrudView.as_view()

