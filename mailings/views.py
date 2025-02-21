from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from .models import Contact, MailingAttempt, Mailings, Message


class ContactListView(ListView):
    model = Contact


class ContactDetailView(DetailView):
    model = Contact


class ContactCreateView(CreateView):
    model = Contact
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("mailings:contact_list")


class ContactUpdateView(UpdateView):
    model = Contact
    fields = ["email", "full_name", "comment"]

    def get_success_url(self):
        return reverse("mailings:contact_detail", kwargs={"pk": self.object.pk})


class ContactDeleteView(DeleteView):
    model = Contact
    success_url = reverse_lazy("mailings:contact_list")


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ["subject", "body"]
    success_url = reverse_lazy("mailings:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]

    def get_success_url(self):
        return reverse("mailings:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailings:message_list")


class MailingsListView(ListView):
    model = Mailings


class MailingsDetailView(DetailView):
    model = Mailings


class MailingsCreateView(CreateView):
    model = Mailings
    fields = ["first_sending", "end_sending", "status", "message", "contact"]
    success_url = reverse_lazy("mailings:mailings_list")


class MailingsUpdateView(UpdateView):
    model = Mailings
    fields = ["first_sending", "end_sending", "status", "message", "contact"]

    def get_success_url(self):
        return reverse("mailings:mailings_detail", kwargs={"pk": self.object.pk})


class MailingsDeleteView(DeleteView):
    model = Mailings
    success_url = reverse_lazy("mailings:mailings_list")


class SendMailingView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailings, pk=pk)
        for contact in mailing.contact.all():
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    "rmiftyaeva@mail.ru",
                    [contact.email],
                    fail_silently=False,
                )
                status = "Успешно"
                server_response = "Письмо отправлено успешно."
            except Exception as e:
                status = "Не успешно"
                server_response = str(e)

            MailingAttempt.objects.create(mailing=mailing, status=status, server_response=server_response)
        return render(request, "mailings/mailing_statistics.html", {"mailing": mailing})


class HomeView(TemplateView):
    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_mailings"] = Mailings.objects.count()
        context["count_active_mailings"] = Mailings.objects.filter(status="started").count()
        context["unique_contacts"] = Contact.objects.count()
        return context
