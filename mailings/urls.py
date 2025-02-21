from django.urls import path
from mailings.apps import MailingsConfig
from .views import (
    ContactListView,
    ContactDetailView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MailingsListView,
    MailingsDetailView,
    MailingsCreateView,
    MailingsUpdateView,
    MailingsDeleteView,
)


app_name = MailingsConfig.name


urlpatterns = [
    path("contact/", ContactListView.as_view(), name="contact_list"),
    path("contact/<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    path("contact/create/", ContactCreateView.as_view(), name="contact_create"),
    path("contact/<int:pk>/update", ContactUpdateView.as_view(), name="contact_update"),
    path("contact/<int:pk>/delete", ContactDeleteView.as_view(), name="contact_delete"),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/update", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete", MessageDeleteView.as_view(), name="message_delete"),
    path("mailings/", MailingsListView.as_view(), name="mailings_list"),
    path("mailings/<int:pk>/", MailingsDetailView.as_view(), name="mailings_detail"),
    path("mailings/create/", MailingsCreateView.as_view(), name="mailings_create"),
    path("mailings/<int:pk>/update", MailingsUpdateView.as_view(), name="mailings_update"),
    path("mailings/<int:pk>/delete", MailingsDeleteView.as_view(), name="mailings_delete"),
]