from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class Location(models.Model):
    caretaker = models.ForeignKey(Person, models.CASCADE)
    room_number = models.CharField(max_length=10)

class Asset(models.Model):
    name = models.CharField(max_length=50)
    details = models.TextField()
    contact_person = models.ForeignKey(Person, models.CASCADE)
    expiry_date = models.DateField()
    vendor = models.CharField(max_length=50)

class SoftwareAsset(Asset):
    version = models.CharField(max_length=15)
    license_key = models.CharField(max_length=30)

class PhysicalAsset(Asset):
    location = models.ForeignKey(Location, models.CASCADE)

