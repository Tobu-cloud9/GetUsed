from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import KeywordForm
from .models import Item
from django.views import generic
from django.contrib import messages
from .yahoo import Yahoo
from .merukari import Merukari
from .paypay import PayPay
from .rakuma import Rakuma

class IndexView(generic.FormView):
    template_name = "index.html"
    form_class = KeywordForm
    success_url = reverse_lazy("GetUsed:result")

    def form_valid(self, form):
        keyword, min_price, max_price, category = form.save()
        print(category)
        messages.add_message(self.request, messages.SUCCESS, '登録しました！')
        Merukari().scraping(keyword, min_price, max_price, category)
        PayPay().scraping(keyword, min_price, max_price, category)
        Yahoo().scraping(keyword, min_price, max_price, category)
        Rakuma().scraping(keyword, min_price, max_price, category)
        return super().form_valid(form)



class ResultView(generic.ListView):
    template_name = "result.html"
    model = Item





