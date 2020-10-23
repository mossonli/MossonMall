import time
import random
from rest_framework import serializers
from .models import Goods, ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer

"""
serializers.Serializer 比modelserializer 更加灵活
serializers.Serializer 需要重写update
"""


# 商品详情
class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")  # read_only 只选择不提交
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        "min_value": "商品的数量不能小于1",
        "required": "请选择购买的商品数量",
    })
    print("user1", user)
    # 用的是serializers.Serializer 需要指明queryset modelserializer 就不用指明queryset
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # serializers.Serializer 要重写 create、update 方法
    def create(self, validated_data):
        user = self.context["request"].user
        print("user2", user)
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品的数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


# 订单
class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


# 订单： 详情
class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


# 订单：
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # 订单的信息 只能读不能随便去改
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    @property
    def generate_order_sn(self):
        """ 生成订单id：当前时间+userid+随机数
            view里面获取user： userid=self.request.user.id
        """
        order_sn = "{time_str}{userid}{randomstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                          userid=self.context["request"].user.id,
                                                          randomstr=random.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
