from .models import InwardStock,OutwardStock,Requisition,StockItem
from .models import Requisition,RequisitionItem,CustomRequisition,CustomRequisitionItem
from rest_framework import serializers

class InwardStockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = (
            'id','item','quantity','measure','price'
        )


class OutwardStockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = (
            'id', 'outward_stock','item','quantity','measure','price'
        )    

class InwardStockSerializer(serializers.ModelSerializer):
    inward = InwardStockItemSerializer(many = True)
    class Meta:
        model = InwardStock
        fields = (
            'id',
            'inward',
            'requisition_id',
            'invoice_id',
            'comment',
            'supplier',
            'created_by')
    
    def create(self, validated_data):
        inward_data = validated_data.pop('inward')
        inwardStock = InwardStock.objects.create(**validated_data)

        for i in inward_data:
            StockItem.objects.create(inward_stock = inwardStock, **i)
        
        return inwardStock

    def update(self,instance,validated_data):
        pass

class OutwardStockSerializer(serializers.ModelSerializer):
    outward = InwardStockItemSerializer(many = True)
    class Meta:
        model = OutwardStock
        fields = (
            'id',
            'outward',
            'requisition_id',
            'comment',
            'consumer',
            'created_by')

    def create(self, validated_data):
        outward_data = validated_data.pop('outward')
        outwardStock = OutwardStock.objects.create(**validated_data)

        for i in outward_data:
            StockItem.objects.create(outward_stock = outwardStock, **i)
        
        return outwardStock

    def update(self,instance,validated_data):
        pass


class RequisitionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitionItem
        fields = (
            'id','requisition','item','measure','quantity','price'
        )


class RequisitionSerializer(serializers.ModelSerializer):
    requests = RequisitionItemSerializer(many= True)

    class Meta:
        model = Requisition
        fields = (
            'id','requests','type','status','is_approved','comment'
        )

    def create(self, validated_data):
        request_data = validated_data.pop('requests')
        requisition = Requisition.objects.create(**validated_data)

        for i in request_data:
            RequisitionItem.objects.create(requisition = requisition, **i)
    
        return requisition

    def update(self,instance,validated_data):
        pass


class CustomRequisitionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRequisitionItem
        fields = (
            'id','custom_requisition','custom_item','measure','quantity','price'
        )

class CustomRequistionSerializer(serializers.ModelSerializer):
    custom_requests = CustomRequisitionItemSerializer(many= True)

    class Meta:
        model = CustomRequisition
        fields = (
            'id','custom_requests','type','status','is_approved','comment'
        )

    def create(self, validated_data):
        request_data = validated_data.pop('custom_requests')
        requisition = CustomRequisition.objects.create(**validated_data)

        for i in request_data:
            CustomRequisitionItem.objects.create(custom_requisition = requisition, **i)
    
        return requisition

    def update(self,instance,validated_data):
        pass