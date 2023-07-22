from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    subject = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Subject"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Message", "class": "message"})
    )
