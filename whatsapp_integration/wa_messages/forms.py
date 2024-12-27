from django import forms

class LoginForm(forms.Form):
    """
        Form for user login. Collects email and password.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True,
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True,
        label='Password'
    )

class SendMessageForm(forms.Form):
    """
       Form for sending a WhatsApp message. Collects phone number and message content.
    """
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
        label='Phone Number'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}),
        label='Message'
    )
