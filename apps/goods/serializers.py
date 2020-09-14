from rest_framework import serializers

from .models import Goods, GoodsCategory


# class GoodSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#
#     def create(self, validated_data):
#         """
#         通过serializer操作model，操作数据库数据
#         :param validated_data: serializer的字段(类似model的字段)
#         :return:
#         """
#         return Goods.objects.create(**validated_data)


class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    """
    modelserializer 和modelform的用法类似
    """
    category = GoodsCategorySerializer()  # category 是 goods里面的外键
    # images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = ('name', 'click_num', 'market_price', 'add_time', 'category')
        # fields = "__all__"    # 序列化所有的字段

# class GoodsCategorySerializer(serializers.ModelSerializer):
#     """
#     商品分配序列化
#     """
#     class Meta:
#         model = GoodsCategory
#         fields = "__all__"
