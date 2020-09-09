## 1 普通方式[非restful]
`urls.py`
```python
urlpatterns = [
    re_path('goods/$', GoodListView.as_view(), )
]
```
`views_base.py`
```python
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
        json_list = []
        for good in goods:
            json_dict = {}
            json_dict["name"] = good.name
            json_dict["category"] = good.category
            json_dict["market_price"] = good.market_price
            json_list.append(json_dict)
        from django.http import HttpResponse
        import json
        return HttpResponse(json.dumps(json_list), content_type="application/json")
```
`访问`
```text
http://127.0.0.1:8000/;goods/
```