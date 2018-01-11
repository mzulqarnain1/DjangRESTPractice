from django.db import models


GENDERS = (
    ('1', 'male'),
    ('2', 'female')
)


# Create your models here.
class PropertyType(models.Model):
    """

    """
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Status(models.Model):
    """

    """
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Owner(models.Model):
    """

    """
    cnic = models.CharField(max_length=16)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDERS, default=1)

    def __str__(self):
        return self.name


class Property(models.Model):
    """

    """
    address = models.TextField(max_length=500)
    type = models.ForeignKey(PropertyType)
    owner = models.ForeignKey(Owner)
    status = models.ForeignKey(Status)
    parentProperty = models.ForeignKey('api.Property', blank=True, null=True)

    def __str__(self):
        return self.address
