from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate    #　追加

from .forms import UserCreateForm


class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('GetUsed:index')   # 変更

    # 以下追加
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response