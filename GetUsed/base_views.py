from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import KeywordForm
from .models import Search
from django.views import generic
from django.contrib import messages



class IndexView(generic.FormView):
    template_name = "index.html"
    form_class = KeywordForm
    success_url = reverse_lazy("GetUsed:result")

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, '登録しました！')
        return super().form_valid(form)


class ResultView(generic.TemplateView):
    template_name = "result.html"



