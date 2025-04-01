from django import forms

from .models import Contact, Mailings, Message


class MailingsForm(forms.ModelForm):
    class Meta:
        model = Mailings
        fields = ["first_sending", "end_sending", "status", "message", "contact"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["email", "full_name", "comment"]
