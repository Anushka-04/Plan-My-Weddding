from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

ACTIVE = (("active", "active"), (" ", "default"))

class VendorType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

    def get_absolute_url(self):
    	return reverse("home:vendor", kwargs={"slug": self.type_name})


class Vendor(models.Model):
	type = models.ForeignKey(VendorType, on_delete=models.CASCADE, blank=True, null=True)
	title = models.CharField(max_length=200)
	image = models.ImageField(upload_to='Vendors')
	address = models.CharField(max_length=200)
	contact = models.CharField(max_length=10, unique = True)
	owner = models.CharField(max_length=200)
	slug = models.CharField(max_length=50)
	avg_price = models.IntegerField()
	desc = models.TextField()

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("home:vendor", kwargs={"slug": self.slug})


	def get_type(self):
		return reverse("home:VendorType", kwargs={"slug": self.slug})


	def get_add_to_list(self):
		return reverse("home:add-to-list", kwargs={"slug": self.slug})


class Slider(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Sliders')
    rank = models.IntegerField()
    status = models.CharField(choices=ACTIVE, max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name


class AddVendor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    added = models.BooleanField(default=False)


    def __str__(self):
        return self.vendor.title



class Add(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendors = models.ManyToManyField(AddVendor)
    added = models.BooleanField(default=False)
    added_date = models.DateTimeField()
    slug=models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
