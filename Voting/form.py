from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

username_validator = RegexValidator(
    regex=r'^[\w.@+\-/]+$',
    message='Enter a valid registration number. This value may contain only letters, numbers, and @/./+/-/_/ slashes characters.',
)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Registration Number"
        self.fields['username'].help_text = "Required. 150 characters or fewer. Letters, digits and @/./+/-/_/ slashes only."
        self.fields['username'].validators = [username_validator]
        self.fields['username'].error_messages = {
            'unique': "A user with that registration number already exists.",
        }

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['username'].label = "Registration Number"
        self.fields['password'].widget.attrs.update({'autocomplete': 'new-password'})