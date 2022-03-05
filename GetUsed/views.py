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

shops = [Merukari(), PayPay(), HardOff(), Rakuma(), Yahoo()]

class IndexView(generic.FormView):
    model = Item
    template_name = "GetUsed/index.html"
    form_class = KeywordForm
    success_url = reverse_lazy("GetUsed:result")

    def form_valid(self, form):
        user_id = self.request.user
        keyword, min_price, max_price, category, status, quality = form.save(user_id)
        Item.objects.all().delete()
        for shop in shops:
            shop.scraping(keyword, min_price, max_price, category, status, quality)
        return super().form_valid(form)



class ResultView(generic.ListView):
    template_name = "GetUsed/result.html"
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(context)

        return context

class MyPageView(generic.ListView):
    template_name = "GetUsed/mypage.html"
    model = Search

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('keyword', None):
            self.keyword = self.request.POST.get('keyword', None)

        if self.request.POST.get('min_price', None):
            self.min_price = self.request.POST.get('min_price', None)

        if self.request.POST.get('max_price', None):
            self.max_price = self.request.POST.get('max_price', None)

        if self.request.POST.get('category', None):
            self.category = self.request.POST.get('category', None)

        if self.request.POST.get('status', None):
            self.status = self.request.POST.get('status', None)

        if self.request.POST.get('quality', None):
            self.quality = self.request.POST.get('quality', None)

        Item.objects.all().delete()

        for shop in shops:
            shop.scraping(self.keyword, self.min_price, self.max_price, self.category, self.status, self.quality)
        return redirect('GetUsed:result')



