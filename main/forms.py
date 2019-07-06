from django import forms
from django.core.exceptions import ValidationError
from .models import Review

class SearchForm(forms.Form):
	query=forms.CharField()

class ReviewForm(forms.ModelForm):
	class Meta:
		model=Review
		fields=['ratings','detail']
	def clean_ratings(self):
		ratings=self.cleaned_data['ratings']
		if ratings > 5.0 or ratings < 0.0:
			raise ValidationError("Ratings should be between 0.0 to 5.0 icluding")
		return ratings
			