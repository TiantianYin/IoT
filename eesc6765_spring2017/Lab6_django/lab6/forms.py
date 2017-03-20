from django import forms

class SrcForm(forms.Form):
	CHOICES = (
		("New York", "New York"),
		("San Diego", "San Diego"),
	)
	srcCity = forms.CharField(label='Start Point', widget=forms.Select(attrs={'class':'form-control'}, choices=CHOICES))

class DesForm(forms.Form):
	CHOICES = (
		("New York", "New York"),
		("San Diego", "San Diego"),
	)
	desCity = forms.CharField(label='Destination', widget=forms.Select(attrs={'class':'form-control'}, choices=CHOICES))

