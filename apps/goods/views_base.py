import json
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from goods.models import Goods

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)



class GoodListView(View):
    def get(self, request):
        """
        通过django的view实现商品的列表页
        :param request:
        :return:
        """
        goods = Goods.objects.all()[:10]
        json_list = []
        # 序列化方式1
        # for good in goods:
        #     json_dict = {}
        #     json_dict["name"] = good.name
        #     json_dict["category"] = good.category
        #     json_dict["market_price"] = good.market_price
        #     json_list.append(json_dict)
        # return HttpResponse(json.dumps(json_data), content_type="application/json")

        # 序列化方式2
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        # return HttpResponse(json.dumps(json_data), content_type="application/json")
        # 序列化方式3
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        # return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(json_data, safe=False)
