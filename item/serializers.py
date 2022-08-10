from rest_framework import serializers
from item.models import Category, Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            )


class ItemSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    class Meta:
        model = Item
        fields = (
            'id',
            'item_code',
            'category',
            'name',
            'description',
            'initail_measure',
            'initail_price',
            'slug',
            'is_published',
            'date_created',
            'get_inward_stock_total',
            'get_outward_stock_total',
            )

