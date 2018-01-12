"""
This module contains our models schema for all the entities
of our application.
"""
from django.db import models
from django.contrib.auth.models import User


class PropertyType(models.Model):
    """
    This model represents structure of a Property Type.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Status(models.Model):
    """
    This model represents structure of a Property Status.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Property(models.Model):
    """
    This model represents structure of a Property and what type of information
    is required to create a Property object.
    """
    address = models.TextField(max_length=500)
    type = models.ForeignKey(PropertyType)
    status = models.ForeignKey(Status, default=None, null=True)
    parentProperty = models.ForeignKey('api.Property', blank=True, null=True)
    owner = models.ForeignKey('auth.User', related_name='properties',
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.address
