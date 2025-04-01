from django.urls import path

from mailings.apps import MailingsConfig

from .views import (ContactCreateView, ContactDeleteView, ContactDetailView, ContactListView, ContactUpdateView,
                    HomeView, MailingAttemptView, MailingDisableView, MailingEnableView, MailingsCreateView,
                    MailingsDeleteView, MailingsDetailView, MailingsListView, MailingsUpdateView, MessageCreateView,
                    MessageDeleteView, MessageDetailView, MessageListView, MessageUpdateView, SendMailingView,
                    StatisticsView)

app_name = MailingsConfig.name


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
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
    path("send-mailing/<int:pk>/", SendMailingView.as_view(), name="send_mailing"),
    path("statistics/", StatisticsView.as_view(), name="statistics"),
    path("mailings/<int:pk>/statistics/", MailingAttemptView.as_view(), name="mailing_statistics"),
    path("mailings/<int:pk>/statistics/", MailingAttemptView.as_view(), name="mailing_statistics"),
    path("mailings/<int:pk>/disable/", MailingDisableView.as_view(), name="disable_mailing"),
    path("mailings/<int:pk>/enable/", MailingEnableView.as_view(), name="enable_mailing"),
]
