from django import forms
from django.contrib.auth.models import User
from .models import Request, Students, Books, User

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    college = forms.CharField(max_length=35)
    student_id = forms.CharField(max_length=55)
    Registration_Number = forms.CharField(max_length=25)
    course = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)
    gender = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'gender','college', 'course', 'status', 'student_id', 'Registration_Number','email','password1','password2']


class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name',)

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2')


class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['first_name','middle_name','Surname','email', ]


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title','isbn','description','author','publisher', ]


# address of shipment
class StudentInfoForm(forms.Form):
    Email = forms.EmailField()
    Mobile = forms.IntegerField()
    Address = forms.CharField(max_length=500)


class RequestForm(forms.ModelForm):
    class Meta:
        model= Request
        fields=['status']