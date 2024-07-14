from django.core.exceptions import ValidationError
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField()
    creditsUrl = models.URLField(blank=True, null=True)
    creditsShortUrl = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        if self.creditsShortUrl and not self.creditsUrl:
            raise ValidationError('You can\'t set the creditsShortUrl field without setting'
                                  'the default creditsUrl field.')

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Project(models.Model):
    index = models.IntegerField()
    hidden = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    image = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    def __str__(self):
        return self.title


class Experience(models.Model):
    index = models.IntegerField()
    hidden = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    period = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    urlShort = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=1023)
    technologies = models.ManyToManyField(Technology, blank=True)

    def clean(self):
        if self.urlShort and not self.url:
            raise ValidationError('You can\'t set the urlShort field without setting the default url field.')

    def __str__(self):
        return f"{self.title} ({self.organisation})"


class WorkItem(models.Model):
    index = models.IntegerField()
    hidden = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    projects = models.ManyToManyField(Project, blank=True)
    experiences = models.ManyToManyField(Experience, blank=True)
    showProjects = models.BooleanField(default=False)
    showExperiences = models.BooleanField(default=False)

    def clean(self):
        if self.showProjects == self.showExperiences:
            raise ValidationError("You must either set showProjects or showExperiences, but not both.")

    def __str__(self):
        return self.title


class Work(models.Model):
    content_type = models.CharField(max_length=255, default='work')
    items = models.ManyToManyField(WorkItem)

    def __str__(self):
        return self.content_type


class Hero(models.Model):
    content_type = models.CharField(max_length=255, default='hero')
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    callToActionContent = models.CharField(max_length=255)
    backgroundImage = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return self.content_type


class About(models.Model):
    content_type = models.CharField(max_length=255, default='about')
    image = models.ForeignKey(File, on_delete=models.CASCADE, related_name='image')
    imageResponsive = models.ForeignKey(
        File, on_delete=models.CASCADE, related_name='imageResponsive', blank=True, null=True
    )
    description = models.CharField(max_length=1023)

    def __str__(self):
        return self.content_type


class Footer(models.Model):
    content_type = models.CharField(max_length=255, default='footer')
    title = models.CharField(max_length=255)
    subTitle = models.CharField(max_length=255)
    showLocation = models.BooleanField(default=True)
    showSocials = models.BooleanField(default=True)
    showEmail = models.BooleanField(default=True)
    showResume = models.BooleanField(default=True)

    def __str__(self):
        return self.content_type


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    locale = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ForeignKey(File, on_delete=models.CASCADE, related_name='logo')
    resume = models.ForeignKey(File, on_delete=models.CASCADE, related_name='resume', blank=True, null=True)
    hero = models.OneToOneField(
        Hero, on_delete=models.CASCADE
    )
    about = models.OneToOneField(
        About, on_delete=models.CASCADE
    )
    work = models.OneToOneField(
        Work, on_delete=models.CASCADE
    )
    footer = models.OneToOneField(
        Footer, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.pk and User.objects.exists():
            raise ValidationError('There can be only one User instance')
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Social(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    index = models.IntegerField()
    hidden = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    pseudo = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    image = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.idUser.name})"
