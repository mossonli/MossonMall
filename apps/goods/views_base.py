from django.views.generic.base import View
from goods.models import Goods
class GoodListView(View):
    def get(self, request):
        """
        通过django的view实现商品的列表页
        :param request:
        :return:
        """
        goods = Goods.objects.all()[:10]
