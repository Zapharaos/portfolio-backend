from django.core.exceptions import ValidationError
from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='images/')

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    index = models.IntegerField()
    description = models.CharField(max_length=1023)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Experience(models.Model):
    title = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    period = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    urlShort = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=1023)
    technologies = models.ManyToManyField(Technology, blank=True)
    index = models.IntegerField()
    hidden = models.BooleanField(default=False)

    def clean(self):
        if self.urlShort and not self.url:
            raise ValidationError('You cannot set the urlShort field without setting the default url field.')

    def __str__(self):
        return self.title


class Hero(models.Model):
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    callToActionContent = models.CharField(max_length=255)
    backgroundImage = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class About(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='image')
    imageResponsive = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='imageResponsive', blank=True, null=True
    )
    description = models.CharField(max_length=1023)

    def __str__(self):
        return str(self.id)


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
    hero = models.OneToOneField(
        Hero, on_delete=models.CASCADE
    )
    about = models.OneToOneField(
        About, on_delete=models.CASCADE
    )
    footer = models.OneToOneField(
        Footer, on_delete=models.CASCADE
    )
    projects = models.ManyToManyField(Project, blank=True)

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
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # TODO
    todo = models.CharField(max_length=7)  # e.g., #FFFFFF

    def __str__(self):
        return self.name
