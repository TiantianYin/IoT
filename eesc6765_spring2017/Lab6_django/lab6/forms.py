from django import forms

class SrcForm(forms.Form):
	CHOICES = (
		("chicago, il", "Chicago"),
		("st louis, mo", "St Louis"),
		("los angeles, ca", "Los Angeles"),
		("kingman, az", "Kingman"),
		("oklahoma city, ok", "Oklahoma City"),
	)
	srcCity = forms.CharField(label='Start Point', widget=forms.Select(attrs={'class':'form-control'}, choices=CHOICES))

class DesForm(forms.Form):
	CHOICES = (
		("chicago, il", "Chicago"),
		("st louis, mo", "St Louis"),
		("los angeles, ca", "Los Angeles"),
		("kingman, az", "Kingman"),
		("oklahoma city, ok", "Oklahoma City"),
	)
	desCity = forms.CharField(label='Destination', widget=forms.Select(attrs={'class':'form-control'}, choices=CHOICES))

