from django import forms
from .models import Publisher, Review, Book

search_choice = (
    ('Title', "Title"), ("Contributor", "Contributor")

)


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover', 'sample']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        exclude = ['book', 'date_created', 'date_edited']

    rating = forms.IntegerField(min_value=0, max_value=5)


class MainSearch_form(forms.Form):
    search = forms.CharField(required=False)
    title_contributor = forms.ChoiceField(required=False, choices=search_choice)
