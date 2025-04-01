import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER

from .forms import CustomUserCreationForm
from .models import User


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("mailings:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserListView(LoginRequiredMixin, ListView):
    model = User


class UserBlockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        if not request.user.groups.filter(name="Manager").exists():
            raise Http404("У вас нет прав для выполнения этого действия.")
        user.is_active = False
        user.save()
        return redirect(reverse("users:user_list"))


class UserUnlockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        if not request.user.groups.filter(name="Manager").exists():
            raise Http404("У вас нет прав для выполнения этого действия.")
        user.is_active = True
        user.save()
        return redirect(reverse("users:user_list"))
