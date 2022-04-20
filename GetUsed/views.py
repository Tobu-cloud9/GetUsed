from django.shortcuts import redirect
from django.urls import reverse_lazy
from .search_forms import KeywordForm
from .models import Item, Search
from django.views import generic
from .yahoo import Yahoo
from .merukari import Merukari
from .paypay import PayPay
from .rakuma import Rakuma
from django.db.models import Avg, Max, Min

from .hardoff import HardOff

shops = [PayPay()]


class IndexView(generic.FormView):
    model = Item
    template_name = "GetUsed/index.html"
    form_class = KeywordForm
    success_url = reverse_lazy("GetUsed:result")

    def form_valid(self, form):
        user_id = self.request.user
        search = form.save(user_id)
        Item.objects.filter(item_search__username=str(user_id)).delete()
        for shop in shops:
            shop.scraping(search, search.keyword, search.min_price,
                          search.max_price, search.category,
                          search.status, search.quality)
        return super().form_valid(form)


class ResultView(generic.ListView):
    template_name = "GetUsed/result.html"
    model = Item

    # ユーザーごとのデータを表示
    def get_queryset(self):
        user_id = self.request.user
        queryset = Item.objects.filter(item_search__username=str(user_id))
        return queryset

    # 商品の平均価格を返す
    def get_AveragePrice(self, **kwargs):
        AveragePrice = Item.objects.aggregate(Avg('item_price'))
        return int(AveragePrice['item_price__avg'])

    # 商品の最高価格を返す
    def get_MaxPrice(self, **kwargs):
        MaxPrice = Item.objects.aggregate(Max('item_price'))
        return MaxPrice['item_price__max']

    # 商品の最低価格を返す
    def get_MinPrice(self, **kwargs):
        MinPrice = Item.objects.aggregate(Min('item_price'))
        return MinPrice['item_price__min']

    # result.htmlに値を渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avg_price"] = self.get_AveragePrice()
        context["max_price"] = self.get_MaxPrice()
        context["min_price"] = self.get_MinPrice()
        return context


class MyPageView(generic.ListView):
    template_name = "GetUsed/mypage.html"
    model = Search

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('delete_id', None):
            self.delete_id = self.request.POST.get('delete_id', None)

            search_object = Search.objects.filter(id=int(self.delete_id))[0]
            search_object.delete()

            return redirect('GetUsed:mypage')
        if self.request.POST.get('search_id', None):
            self.search_id = self.request.POST.get('search_id', None)

            user_id = self.request.user
            item_model = Item.objects.filter(item_search__username=str(user_id))
            item_model.delete()
            search_object = Search.objects.filter(id=int(self.search_id))[0]
            print(search_object)

            for shop in shops:
                shop.scraping(search_object, search_object.keyword, search_object.min_price, search_object.max_price,
                              search_object.category, search_object.status, search_object.quality)
            return redirect('GetUsed:result')
