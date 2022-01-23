from django.db import models
from django.core.validators import FileExtensionValidator


class Weather(models.Model):
    tmp = models.TextField(primary_key=True)
    pop = models.IntegerField(null=False, default=0)
    pty = models.TextField()
    reh = models.IntegerField(null=False, default=0)
    sky = models.TextField()
    img = models.FileField(upload_to="pictures/%Y/%m/", 
        validators=[FileExtensionValidator(['pdf', 'doc', 'svg'])])
    wsd = models.IntegerField(null=False, default=0)