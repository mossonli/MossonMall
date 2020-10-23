import time
import random
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
# Create your views here.
from utils.permissions import IsOwnerOrReadOnly

from .serialiazers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods

"""
mixins.CreateModelMixin,
mixins.RetrieveModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
mixins.ListModelMixin,
GenericViewSet

viewsets.ModelViewSet 继承了上边所有的mixins
"""


class ShoppingCartVioewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车列表
    create:
        加入购物车
    delete:
        删除购物车物品
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    # queryset = ShoppingCart.objects.all()
    lookup_field = "goods_id"

    # 获取不同的seializer
    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    # 获取当前用户的购物车
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    List：
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # serializer_class = OrderSerializer

    # queryset = ShoppingCart.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    # 结算之后要清空购物车
    def perform_create(self, serializer):
        order = serializer.save()  # save 之前要生成订单号
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order
