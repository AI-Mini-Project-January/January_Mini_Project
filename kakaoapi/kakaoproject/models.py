from django.db import models
from django.db.models.fields import CharField, IntegerField, TextField, FloatField

# Create your models here.

class User(models.Model):
    id = IntegerField(primary_key = True)
    user_identi = models.CharField(max_length=50, null = False, unique = True)
    password = CharField(max_length=50, null=False)
    nickname = CharField(max_length=50, null=False, unique = True)
    age = IntegerField()
    profile_img = TextField()

    class Meta:
        db_table = 'User'
        app_label = 'kakaoproject'
        managed = False