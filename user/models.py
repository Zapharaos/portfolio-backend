from django.core.exceptions import ValidationError
from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # TODO
    todo = models.CharField(max_length=7)  # e.g., #FFFFFF

    def __str__(self):
        return self.name


class User(models.Model):
    hero = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    email = models.EmailField(unique=True)
    logo = models.FileField(upload_to='logos/')
    photo = models.FileField(upload_to='photos/', blank=True, null=True)
    curriculum = models.FileField(upload_to='curriculums/', blank=True, null=True)
    theme_light = models.ForeignKey(Theme, on_delete=models.SET_NULL, blank=True, null=True, related_name='light_theme')
    theme_dark = models.ForeignKey(Theme, on_delete=models.SET_NULL, blank=True, null=True, related_name='dark_theme')

    def save(self, *args, **kwargs):
        if not self.pk and User.objects.exists():
            raise ValidationError('There can be only one User instance')
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class Social(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(unique=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class List(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    index = models.IntegerField(unique=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ListItem(models.Model):
    idList = models.ForeignKey(List, on_delete=models.CASCADE)
    index = models.IntegerField(unique=True)
    organisation = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    menuName = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    period = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=511, blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name
