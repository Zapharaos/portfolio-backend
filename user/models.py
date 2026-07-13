from zoneinfo import available_timezones

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .storage import OverwriteStorage


def validate_timezone(value):
    """Ensure the value is a valid IANA timezone name (e.g. 'Europe/Paris')."""
    if value and value not in available_timezones():
        raise ValidationError('%(value)s is not a valid IANA timezone.', params={'value': value})


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(storage=OverwriteStorage())
    creditsUrl = models.URLField(blank=True, null=True)
    creditsShortUrl = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        if self.creditsShortUrl and not self.creditsUrl:
            raise ValidationError('You can\'t set the creditsShortUrl field without setting'
                                  'the default creditsUrl field.')

    def __str__(self):
        return self.name


@receiver(post_delete, sender=File)
def _delete_file_on_record_delete(sender, instance, **kwargs):
    """Remove the file from storage when its File record is deleted."""
    if instance.file:
        instance.file.delete(save=False)


@receiver(pre_save, sender=File)
def _delete_old_file_on_change(sender, instance, **kwargs):
    """When a File's upload is replaced by a differently-named one, delete the old
    file so it doesn't become an orphan (same-name uploads are overwritten)."""
    if not instance.pk:
        return
    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return
    if old_file and old_file.name != instance.file.name:
        old_file.delete(save=False)


class Technology(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(
        max_length=7, blank=True, default='',
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')],
        help_text='Tag hue as #RRGGBB. Empty = default style.',
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    class ImageFit(models.TextChoices):
        COVER = 'cover', 'Cover (fill, may crop)'
        CONTAIN = 'contain', 'Contain (whole image, padded)'

    index = models.IntegerField()
    hidden = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=50, blank=True, default='',
        help_text='Short badge shown on the card (e.g. "Side project", "Pro"). Empty = no badge.',
    )
    metric = models.CharField(
        max_length=100, blank=True, default='',
        help_text='Short metric shown under the description (e.g. "~6k € ARR", "10k users").',
    )
    isNew = models.BooleanField(default=False, help_text='Show a "New" badge on the card.')
    inProgress = models.BooleanField(
        default=False,
        help_text='Show a "Work in progress" badge on the card.',
    )
    iconFramed = models.BooleanField(
        default=True,
        help_text='Frame the icon (tile + border). Uncheck for a frameless icon.',
    )
    imageFit = models.CharField(
        max_length=10, choices=ImageFit.choices, default=ImageFit.COVER,
        help_text='How the image fills the icon frame (cover = fill/crop, contain = whole image).',
    )
    image = models.ForeignKey(File, on_delete=models.SET_NULL, blank=True, null=True)
    technologies = models.ManyToManyField(Technology, blank=True, through='ProjectTechnology')
    healthUrl = models.URLField(
        blank=True, null=True,
        help_text='Health endpoint to probe periodically. Empty = no check.',
    )
    healthUp = models.BooleanField(
        null=True, default=None, editable=False,
        help_text='Last known state; null = never checked.',
    )
    healthCheckedAt = models.DateTimeField(null=True, default=None, editable=False)
    healthFailures = models.PositiveSmallIntegerField(
        default=0, editable=False,
        help_text='Consecutive failures (guards against false negatives).',
    )

    def save(self, *args, **kwargs):
        # No health URL means no monitoring: clear any stale state so the badge
        # disappears when the admin removes the URL.
        if not self.healthUrl:
            self.healthUp = None
            self.healthFailures = 0
        return super().save(*args, **kwargs)

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

    class IconPosition(models.TextChoices):
        BEFORE = 'before', 'Before label'
        AFTER = 'after', 'After label'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='links')
    kind = models.CharField(max_length=20, choices=Kind.choices)
    url = models.URLField()
    label = models.CharField(
        max_length=255, blank=True, default='',
        help_text='Displayed text; empty = "View".',
    )
    icon = models.ForeignKey(
        File, on_delete=models.SET_NULL, blank=True, null=True, related_name='+',
        help_text='Icon file (SVG or PNG); empty = no icon.',
    )
    iconPosition = models.CharField(
        max_length=10, choices=IconPosition.choices, default=IconPosition.BEFORE,
        help_text='Icon position relative to the label.',
    )
    color = models.CharField(
        max_length=7, blank=True, default='',
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')],
        help_text='Link hue as #RRGGBB (text, border, SVG icon). Empty = default style.',
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
    backgroundImage = models.ForeignKey(File, on_delete=models.PROTECT)

    def __str__(self):
        return self.content_type


class About(models.Model):
    content_type = models.CharField(max_length=255, default='about')
    image = models.ForeignKey(File, on_delete=models.PROTECT, related_name='image')
    imageResponsive = models.ForeignKey(
        File, on_delete=models.SET_NULL, related_name='imageResponsive', blank=True, null=True
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


class Theme(models.Model):
    name = models.CharField(max_length=255, unique=True)
    background = models.CharField(
        max_length=7,
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')],
        help_text='--color-background token as #RRGGBB.',
    )
    text = models.CharField(
        max_length=7,
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')],
        help_text='--color-text token as #RRGGBB.',
    )
    primary = models.CharField(
        max_length=7,
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')],
        help_text='--color-primary token as #RRGGBB.',
    )

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    locale = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(
        max_length=64, blank=True, default='',
        validators=[validate_timezone],
        help_text="IANA timezone (e.g. 'Europe/Paris') for the footer clock; empty = visitor's local time.",
    )
    logo = models.ForeignKey(File, on_delete=models.PROTECT, related_name='logo')
    resume = models.ForeignKey(File, on_delete=models.SET_NULL, related_name='resume', blank=True, null=True)
    theme = models.ForeignKey(
        Theme, on_delete=models.SET_NULL, blank=True, null=True,
        help_text='Active theme; empty = frontend default tokens.',
    )
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
    image = models.ForeignKey(File, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} ({self.idUser.name})"
