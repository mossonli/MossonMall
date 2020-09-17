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

router = DefaultRouter()
router.register(r'goods', GoodListViewSet, basename="goods")
#配置category的url
router.register(r'categorys', GoodsCategoryViewset, basename="categorys")


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
    path('docs/', include_docs_urls(title='路飞')),
    # drf登录的url
    re_path(r'^api-auth/', include('rest_framework.urls')),
    # drf自带的token认证方式
    path(r'api-token-auth/', views.obtain_auth_token),
    # jwt 认证方式
    re_path(r'^login-jwt/', obtain_jwt_token),
    #
    path(r'', include(router.urls)),

]
