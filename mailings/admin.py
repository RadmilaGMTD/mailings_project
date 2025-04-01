from django.contrib import admin

from .models import Contact, Mailings, Message


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment", "owner")
    list_filter = ("full_name",)
    search_fields = ("full_name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "body",
    )


@admin.register(Mailings)
class MailingsAdmin(admin.ModelAdmin):
    list_display = ("id", "first_sending", "end_sending", "status", "message", "owner")
    list_filter = ("status",)
    search_fields = ("status",)
