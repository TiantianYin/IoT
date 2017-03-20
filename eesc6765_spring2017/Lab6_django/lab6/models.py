from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CityWeather(models.Model):
	cityName = models.CharField(max_length = 40)
	cityWeather = models.CharField(max_length = 100)

	def __str__(self):
		return self.cityName

		
