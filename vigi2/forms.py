from django import forms

class RatingForm(forms.Form):
    rating = forms.DecimalField(min_value=1.0, max_value=10.0, decimal_places=1, max_digits=3)

  