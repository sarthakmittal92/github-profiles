from django.db import models

class Profile(models.Model):
	login = models.CharField(max_length=150)
	followers = models.IntegerField()
	updated_at = models.CharField(max_length=150)
	name = models.CharField(max_length=150)

class Repository(models.Model):
	name = models.CharField(max_length=150)
	stars = models.IntegerField()
	profile = models.ForeignKey(Profile,on_delete=models.CASCADE)