from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
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
    color = models.CharField(
        max_length=7, blank=True, default='',
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')],
        help_text='Teinte du tag au format #RRGGBB. Vide = style par défaut.',
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    index = models.IntegerField()
    hidden = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    technologies = models.ManyToManyField(Technology, blank=True, through='ProjectTechnology')

    def __str__(self):
        return self.title


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(fields=['project', 'technology'], name='unique_project_technology'),
        ]

    def __str__(self):
        return f"{self.project.title} — {self.technology.name} (#{self.position})"


class ProjectLink(models.Model):
    class Kind(models.TextChoices):
        GITHUB = 'github', 'GitHub'
        WEBSITE = 'website', 'Website'
        APPSTORE = 'appstore', 'App Store'
        PLAYSTORE = 'playstore', 'Play Store'
        DOCS = 'docs', 'Documentation'
        OTHER = 'other', 'Other'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='links')
    kind = models.CharField(max_length=20, choices=Kind.choices)
    url = models.URLField()
    label = models.CharField(
        max_length=255, blank=True, default='',
        help_text='Texte affiché ; vide = libellé par défaut du kind.',
    )
    icon = models.ForeignKey(
        File, on_delete=models.SET_NULL, blank=True, null=True, related_name='+',
        help_text='Fichier icône (SVG ou PNG) ; vide = icône par défaut du kind.',
    )
    color = models.CharField(
        max_length=7, blank=True, default='',
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')],
        help_text='Teinte du lien au format #RRGGBB (texte, bordure, icône SVG). Vide = style par défaut.',
    )
    index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['index']

    def __str__(self):
        return f"{self.get_kind_display()} ({self.project.title})"


class Experience(models.Model):
    index = models.IntegerField()
    hidden = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    period = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    urlShort = models.URLField(blank=True, null=True)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True, through='ExperienceTechnology')

    def clean(self):
        if self.urlShort and not self.url:
            raise ValidationError('You can\'t set the urlShort field without setting the default url field.')

    def __str__(self):
        return f"{self.title} ({self.organisation})"


class ExperienceTechnology(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(fields=['experience', 'technology'], name='unique_experience_technology'),
        ]

    def __str__(self):
        return f"{self.experience.title} — {self.technology.name} (#{self.position})"


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
    tagline = models.TextField()
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
    description = models.TextField()

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
    color = models.CharField(
        max_length=7, blank=True, default='',
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')],
        help_text='Teinte de l\'icône au format #RRGGBB. Vide = couleur du thème.',
    )

    def __str__(self):
        return f"{self.name} ({self.idUser.name})"
