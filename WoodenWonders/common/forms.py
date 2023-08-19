from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Име"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Имейл"}))
    subject = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Заглавие"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Съобщение", "class": "message"})
    )
