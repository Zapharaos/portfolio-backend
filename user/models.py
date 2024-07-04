from django.core.exceptions import ValidationError
from django.db import models


class SVG(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='svg/')

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # TODO
    todo = models.CharField(max_length=7)  # e.g., #FFFFFF

    def __str__(self):
        return self.name


class Footer(models.Model):
    title = models.CharField(max_length=255)
    subTitle = models.CharField(max_length=255)
    showLocation = models.BooleanField(default=True)
    showSocials = models.BooleanField(default=True)
    showEmail = models.BooleanField(default=True)
    showResume = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    locale = models.CharField(max_length=255, blank=True, null=True)
    footer = models.OneToOneField(
        Footer, on_delete=models.CASCADE, blank=True, null=True
    )

    hero = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    logo = models.FileField(upload_to='logos/')
    photo = models.FileField(upload_to='photos/', blank=True, null=True)
    curriculum = models.FileField(upload_to='curriculums/', blank=True, null=True)
    theme_light = models.ForeignKey(Theme, on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='light_theme')
    theme_dark = models.ForeignKey(Theme, on_delete=models.SET_NULL, blank=True, null=True, related_name='dark_theme')

    def save(self, *args, **kwargs):
        if not self.pk and User.objects.exists():
            raise ValidationError('There can be only one User instance')
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class Social(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    index = models.IntegerField()
    name = models.CharField(max_length=255)
    pseudo = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    svg = models.ForeignKey(SVG, on_delete=models.CASCADE)
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
