from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Имейл"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Съобщение"}))
