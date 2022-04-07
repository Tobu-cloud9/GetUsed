from django.shortcuts import redirect
from django.urls import reverse_lazy
from .search_forms import KeywordForm
from .models import Item, Search
from django.views import generic
from .yahoo import Yahoo
from .merukari import Merukari
from .paypay import PayPay
from .rakuma import Rakuma
from .hardoff import HardOff

shops = [HardOff()]

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
            shop.scraping(search, search.keyword, search.min_price, search.max_price,
                          search.category, search.status, search.quality)
        return super().form_valid(form)


class ResultView(generic.ListView):
    template_name = "GetUsed/result.html"
    model = Item

    def get_queryset(self):
        user_id = self.request.user
        queryset = Item.objects.filter(item_search__username=str(user_id))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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



