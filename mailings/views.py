from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Message, Contact, Mailings
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse


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
