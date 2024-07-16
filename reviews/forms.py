from django import forms

search_choice = (
    ('Title', "Title"), ("Contributor", "Contributor")

)


class MainSearch_form(forms.Form):
    search = forms.CharField(required=False)
    title_contributor = forms.ChoiceField(required=False, choices=search_choice)
