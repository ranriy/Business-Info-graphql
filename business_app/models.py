from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
	name = models.CharField(max_length=200)
	address = models.TextField()
	owners = models.ManyToManyField(User, related_name="ownerships")
	employee_size = models.IntegerField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
