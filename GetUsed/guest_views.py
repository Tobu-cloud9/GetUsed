from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import KeywordForm
from django.views import generic

from .models import Search
from .models import Item
from accounts.models import User

posted_data = {"text": "",
               "select_part": []}

class IndexView(generic.TemplateView, generic.FormView):
    template_name = "index.html"
    form_class = KeywordForm
    success_url = 'result'

    def form_valid(self, form):
        posted_data["text"] = form.data.get("text")
        print("キーワードを取得")
        form.save()
        print("キーワードを保存")
        return super().form_valid(form)

class ResultListView(generic.ListView):
    model = Item
    template_name = "result.html"


    #変数を渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_keyword"] = posted_data["text"]
        return context

