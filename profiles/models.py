from django.db import models


class User(models.Model):
    hero = models.JSONField()
    logo = models.BinaryField()
    description = models.CharField(max_length=255)
    photo = models.BinaryField(blank=True, null=True)
    curriculum = models.FileField(upload_to='curriculums/', blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Portfolio(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)

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

