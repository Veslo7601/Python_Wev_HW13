from django.forms import ModelForm, CheckboxSelectMultiple, Select
from .models import Tag, Autors, Quotes

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class AuthorForm(ModelForm):
    class Meta:
        model = Autors
        fields = ['name', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    class Meta:
        model = Quotes
        fields = ['tags', 'author', 'quote']
        widgets = {
            'tags': CheckboxSelectMultiple(),
            'author': Select()
        }