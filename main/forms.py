from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )
    
    message = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Message',
            'rows': 5
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and ('@' not in email or '.' not in email.split('@')[-1]):
            raise forms.ValidationError("Please enter a valid email address.")
        return email
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message) > 300:
            raise forms.ValidationError("Message cannot exceed 300 characters.")
        return message
