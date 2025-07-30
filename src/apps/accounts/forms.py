"""
class ExampleModelForm(forms.ModelForm):
    field3 = forms.CharField(
        max_length= 100,
        required= True,
        label= "Full Name",
        help_text= "Enter your full name.",
        widget= forms.TextInput(attrs={"placeholder": "John Doe", "class": "form-control"}),
    )
    
    class Meta:
        model = ExampleModel
        fields = ["field1", "field2", "field3"]
        widgets = {
            "field1": forms.TextInput(attrs={"class": "form-control"}),
            "field2": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
        help_texts = {
            "field1": "Enter a value for field1.",
        }
        labels = {
            "field1": "Custom Label for Field1",
        }

    def clean_field1(self):    
        clean_field1 = self.cleaned_data.get("clean_field1")
        if not clean_field1.endswith("@domain.com"):
            raise forms.ValidationError("clean_field1 must be from domain.com")
        return clean_field1
    
    def clean(self):
        cleaned_data = super(ExampleModelForm, self).clean()
        field1 = cleaned_data.get("field1")
        field2 = cleaned_data.get("field2")

        if field1 == field2:
            self.add_error('field1',"field1 is not same as field2")
        return cleaned_data
    
    def save(self):
        # Override or write your own save method
        pass
"""
import uuid
from .models import *  
from django import forms
from .tasks import send_verification_link
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
# Create your forms here.

class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(validators=[validate_password])
    confirm_password = forms.CharField()
    class Meta:
        model = get_user_model()
        fields = ["username","email","password","confirm_password"]
        
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if not self.has_error("password"):
            if password != confirm_password:
                self.add_error('confirm_password',"Password and Confirm Password do not match.")
        return cleaned_data
    
    def save(self, request):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user_obj = get_user_model().objects.create(
            username = username,
            email = email,
        )
        user_obj.is_verified = False
        user_obj.uuid = uuid.uuid4()
        user_obj.set_password(password)
        user_obj.save()
        send_verification_link(request, username, email, user_obj.uuid)
