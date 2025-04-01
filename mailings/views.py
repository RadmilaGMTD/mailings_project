from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from config import settings

from .forms import ContactForm, MailingsForm, MessageForm
from .models import Contact, MailingAttempt, Mailings, Message
from .services import check_user_permission, get_mailings_from_cache


class ContactListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Contact
    permission_required = "mailings.can_view_mailings"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Manager").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


@method_decorator(cache_page(60), name="dispatch")
class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Manager").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        check_user_permission(self.request.user, obj)
        return obj


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy("mailings:contact_list")


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm

    def form_valid(self, form):
        contact = self.get_object()
        if self.request.user != contact.owner:
            return HttpResponseForbidden("У вас нет прав на редактирование контакта.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailings:contact_detail", kwargs={"pk": self.object.pk})


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy("mailings:contact_list")

    def post(self, request, *args, **kwargs):
        contact = self.get_object()
        if not request.user == contact.owner:
            return HttpResponseForbidden("У вас нет прав на удаление контакта.")
        contact.delete()
        return redirect("mailings:mailings_list")


class MessageListView(ListView):
    model = Message


@method_decorator(cache_page(60), name="dispatch")
class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse("mailings:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailings:message_list")


class MailingsListView(LoginRequiredMixin, ListView):
    model = Mailings

    def get_queryset(self):
        queryset = get_mailings_from_cache()
        if self.request.user.groups.filter(name="Manager").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


@method_decorator(cache_page(60), name="dispatch")
class MailingsDetailView(LoginRequiredMixin, DetailView):
    model = Mailings

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Manager").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        check_user_permission(self.request.user, obj)
        return obj


class MailingsCreateView(LoginRequiredMixin, CreateView):
    model = Mailings
    form_class = MailingsForm
    success_url = reverse_lazy("mailings:mailings_list")

    def form_valid(self, form):
        mailing = form.save(commit=False)
        user = self.request.user
        status = Mailings.STATUS_CREATED
        mailing.owner = user
        mailing.status = status
        mailing.save()
        return super().form_valid(form)


class MailingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailings
    form_class = MailingsForm

    def form_valid(self, form):
        mailing = self.get_object()
        if self.request.user != mailing.owner:
            return HttpResponseForbidden("У вас нет прав на редактирование рассылки.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailings:mailings_detail", kwargs={"pk": self.object.pk})


class MailingsDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailings
    success_url = reverse_lazy("mailings:mailings_list")

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        if not request.user == mailing.owner:
            return HttpResponseForbidden("У вас нет прав на удаление рассылки.")
        mailing.delete()
        return redirect("mailings:mailings_list")


class SendMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailings, pk=pk)
        if mailing.status == Mailings.STATUS_COMPLETED:
            return HttpResponseForbidden(f"Рассылка не может быть отправлена, так как её статус {mailing.status}")
        if mailing.status == Mailings.STATUS_CREATED:
            mailing.status = Mailings.STATUS_STARTED
            mailing.first_sending = timezone.now()
            mailing.save()
            for contact in mailing.contact.all():
                attempt = MailingAttempt(mailing=mailing)
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[contact.email],
                        fail_silently=False,
                    )
                    attempt.status = MailingAttempt.STATUS_SUCCESSFUL
                    attempt.server_response = "Письмо отправлено успешно."
                except Exception as e:
                    attempt.status = MailingAttempt.STATUS_NOT_SUCCESSFUL
                    attempt.server_response = str(e)
                attempt.save()
            mailing.status = Mailings.STATUS_COMPLETED
            mailing.end_sending = timezone.now()
            mailing.save()
        mailing_attempts = MailingAttempt.objects.filter(mailing=mailing)
        return render(
            request, "mailings/mailing_statistics.html", {"mailing": mailing, "mailing_attempts": mailing_attempts}
        )


class HomeView(TemplateView):
    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_mailings"] = Mailings.objects.count()
        context["count_active_mailings"] = Mailings.objects.filter(status="started").count()
        context["unique_contacts"] = Contact.objects.count()
        return context


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "mailings/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        successful_mailings = MailingAttempt.objects.filter(
            mailing__owner=user, status=MailingAttempt.STATUS_SUCCESSFUL
        )
        unsuccessful_mailings = MailingAttempt.objects.filter(
            mailing__owner=user, status=MailingAttempt.STATUS_NOT_SUCCESSFUL
        )
        user_mailings = Mailings.objects.filter(owner=user)

        mailings = Mailings.objects.filter(owner=user)

        context["successful_mailings"] = successful_mailings
        context["unsuccessful_mailings"] = unsuccessful_mailings
        context["count_successful_mailings"] = successful_mailings.count()
        context["count_unsuccessful_mailings"] = unsuccessful_mailings.count()
        context["count_total_mailings"] = user_mailings.count()
        context["count_messages"] = mailings.values("message").count()
        return context


class MailingAttemptView(TemplateView):
    model = MailingAttempt
    template_name = "mailings/mailing_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs["pk"]
        mailing = Mailings.objects.get(id=pk)
        context["mailing"] = mailing
        context["mailing_attempts"] = MailingAttempt.objects.filter(mailing=mailing)
        return context


class MailingDisableView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailings, id=pk)
        check_user_permission(request.user, mailing)  # Проверяем права доступа
        mailing.is_active = False
        mailing.save()
        return redirect(reverse("mailings:mailings_list"))


class MailingEnableView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailings, id=pk)
        check_user_permission(request.user, mailing)  # Проверяем права доступа
        mailing.is_active = True
        mailing.save()
        return redirect(reverse("mailings:mailings_list"))
