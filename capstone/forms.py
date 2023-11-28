from django import forms
from .models import Show, Review, Rating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        