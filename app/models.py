from django.db.models import (
    Model, ForeignKey, CharField, TextField, DateField, BooleanField, 
    ManyToManyField, SET_NULL, CASCADE
)
from django.contrib.auth.models import User

class Location(Model):
    manager = ForeignKey(User, SET_NULL, null=True)
    room_number = CharField(max_length=10)
    def __str__(self):
        return 'room number {}'.format(self.room_number)

class Asset(Model):
    name = CharField(max_length=50)
    details = TextField()
    contact_person = ForeignKey(User, SET_NULL, related_name='asset_manage_set', null=True)
    expiry_date = DateField()
    vendor = CharField(max_length=50)
    users = ManyToManyField(User, related_name='asset_use_set')
    def __str__(self):
        return self.name

class SoftwareAsset(Asset):
    version = CharField(max_length=15)
    license_key = CharField(max_length=30)

class PhysicalAsset(Asset):
    location = ForeignKey(Location, SET_NULL, null=True)

class AssetRequest(Model):
    creator = ForeignKey(User, CASCADE, related_name='created_request_set')
    approved = BooleanField(default=False)
    rejected = BooleanField(default=False)
    details = TextField()

class AssetAccessRequest(AssetRequest):
    requested_asset = ForeignKey(Asset, CASCADE)

class AssetAcquireRequest(AssetRequest):
    requested_asset_detail = TextField()
