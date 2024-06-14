from django.core.exceptions import ValidationError
from django.db import models


class User(models.Model):
    hero = models.CharField(max_length=255)
    logo = models.BinaryField()
    description = models.CharField(max_length=255)
    photo = models.BinaryField(blank=True, null=True)
    curriculum = models.FileField(upload_to='curriculums/', blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    background = models.CharField(max_length=7)  # e.g., #FFFFFF
    color = models.CharField(max_length=7)  # e.g., #000000

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    theme_light = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, related_name='light_theme_portfolios')
    theme_dark = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, related_name='dark_theme_portfolios')

    def __str__(self):
        return str(self.id)


class Social(models.Model):
    name = models.CharField(max_length=255)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class List(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    index = models.IntegerField()
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ListItem(models.Model):
    idList = models.ForeignKey(List, on_delete=models.CASCADE)
    index = models.IntegerField()
    organisation = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    menuName = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    period = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DefaultUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='default_user')

    def save(self, *args, **kwargs):
        if not self.pk and DefaultUser.objects.exists():
            raise ValidationError('There can be only one DefaultUser instance')
        return super(DefaultUser, self).save(*args, **kwargs)

    def __str__(self):
        return f'Default user: {self.user.id}'
