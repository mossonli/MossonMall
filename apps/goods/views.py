from django.http import Http404
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods
from .serializers import GoodsSerializer
from .filters import GoodsFilter


# Create your views here.

# class GoodListView(APIView):
#     """
#     List all goods.
#     """
#
#     def get(self, request, format=None):
#         goods = Goods.objects.all()
#         goods_serializer = GoodsSerializer(goods, many=True)  # many=True 表示这个是一个query_set对象有多个good
#         return Response(goods_serializer.data)
#
#     # 新建数据
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 定义分页
class GoodsPagination(PageNumberPagination):
    page_size = 10  # 每页展示的数据量
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 100


# 利用drf的viewset
class GoodListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，分页、搜索、过滤、排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer  # 序列化类
    pagination_class = GoodsPagination  # 分页
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)   # 过滤 查找 排序
    filter_class = GoodsFilter                  # 过滤类
    search_fields = ("name", "goods_brief", "goods_desc")   # 搜索条件
    ordering_fields = ("sold_num", "add_time")



