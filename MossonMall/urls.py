"""MossonMall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
import xadmin

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from MossonMall.settings import MEDIA_ROOT
# from goods.views_base import GoodListView
# from goods.views import GoodListView
from goods.views import GoodListViewSet, GoodsCategoryViewset
from users.views import SmsCodeViewset, UserRegViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset,AddressViewset
from trade.views import ShoppingCartVioewset, OrderViewset

router = DefaultRouter()
router.register(r'goods', GoodListViewSet, basename="goods")
# 配置category的url
router.register(r'categorys', GoodsCategoryViewset, basename="categorys")
# 验证码发送
router.register(r'codes', SmsCodeViewset, basename="codes")
# 用户注册
router.register(r'users', UserRegViewset, basename="users")
# 用户收藏
router.register(r'userfavs', UserFavViewset, basename="userfavs")
# 留言
router.register(r'messages', LeavingMessageViewset, basename="messages")
# 收货地址
router.register(r'address', AddressViewset, basename="address")
# 购物车
router.register(r'shopcarts', ShoppingCartVioewset, basename="shopcarts")
# 订单
router.register(r'orders', OrderViewset, basename="orders")

goods_list = GoodListViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 商品列表
    # re_path(r'goods/$', GoodListView.as_view(), name="gods-list"),
    # 程序的说明文档
    re_path(r'^docs/', include_docs_urls(title='路飞')),
    # drf登录的url
    re_path(r'^api-auth/', include('rest_framework.urls')),
    # drf自带的token认证方式
    path(r'api-token-auth/', views.obtain_auth_token),
    # jwt 认证方式
    re_path(r'^login-jwt/', obtain_jwt_token),
    #
    path(r'', include(router.urls)),

]
