from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    qty = serializers.IntegerField(min_value=1)


class CartSetQtySerializer(serializers.Serializer):
    qty = serializers.IntegerField(min_value=0)  # 0 = remove
