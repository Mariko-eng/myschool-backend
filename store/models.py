from django.db import models
from item.models import Item, Supplier, Consumer
from django.contrib.auth.models import User

class InwardStock(models.Model):
    supplier = models.ForeignKey(Supplier,related_name="supplier", null=True,on_delete=models.SET_NULL,blank=True)
    requisition_id = models.CharField(max_length=100,blank=True,null=True) #Id for procuring the stock
    invoice_id = models.CharField(max_length=100,blank=True,null=True) #invoice from the supplier
    comment = models.TextField('comments', blank=True,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(null=True,blank=True)


class OutwardStock(models.Model):
    consumer = models.ForeignKey(Consumer,related_name="consumer", null=True,on_delete=models.SET_NULL,blank=True)
    requisition_id = models.CharField(max_length=100,blank=True,null=True)
    comment = models.TextField('comments', blank=True,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(null=True,blank=True)


class StockItem(models.Model):
    inward_stock = models.ForeignKey(InwardStock, related_name="inward",null=True,on_delete=models.SET_NULL)
    outward_stock = models.ForeignKey(OutwardStock,related_name="outward",null=True,on_delete=models.SET_NULL)
    item = models.ForeignKey(Item,related_name="stock_items",null=True,on_delete=models.SET_NULL)
    measure = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12,decimal_places=3)


class Requisition(models.Model):
    TYPES = [
        ('NEW_ITEM','NEW_ITEM'), 
        ('OUT_OF_STOCK','OUT_OF_STOCK'),
        ('REPLACE_EXISTING', 'REPLACE_EXISTING'),
        ('EMERGENCY','EMERGENCY'), 
        ('REQUEST_BY_CONSUMER', 'REQUEST_BY_CONSUMER'),
    ]
    type = models.CharField(choices=TYPES,max_length=100,blank=True,null=True)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(default="pending",max_length=100,blank=True,null=True)
    comment = models.TextField('comments', blank=True,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(null=True,blank=True)


class RequisitionItem(models.Model):
    requisition = models.ForeignKey(Requisition,related_name='requests',null=True,on_delete=models.SET_NULL)
    item = models.ForeignKey(Item,null=True,on_delete=models.SET_NULL)
    measure = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    price = models.DecimalField(max_digits=12, decimal_places=3, null=True)

    def get_total_price(self):
        return self.price * self.quantity

class CustomRequisition(models.Model):
    TYPES = [
        ('NEW_ITEM','NEW_ITEM'), 
        ('OUT_OF_STOCK','OUT_OF_STOCK'),
        ('REPLACE_EXISTING', 'REPLACE_EXISTING'),
        ('EMERGENCY','EMERGENCY'), 
        ('REQUEST_BY_CONSUMER', 'REQUEST_BY_CONSUMER'),
    ]
    type = models.CharField(choices=TYPES,max_length=100,blank=True,null=True)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(default="pending",max_length=100,blank=True,null=True)
    comment = models.TextField('comments', blank=True,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(null=True,blank=True)

class CustomRequisitionItem(models.Model):
    custom_requisition = models.ForeignKey(CustomRequisition,related_name='custom_requests',null=True,on_delete=models.SET_NULL)
    custom_item = models.CharField(max_length=200,null=True)
    measure = models.CharField(max_length=100,null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    price = models.DecimalField(max_digits=12, decimal_places=3, null=True)

    def get_total_price(self):
        return self.price * self.quantity