from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year is None or not isinstance(year, int):
            raise forms.ValidationError("Please enter a valid year.")
        return year


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('date_of_birth', 'profile_photo')