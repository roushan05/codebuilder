# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Data(models.Model):
    path = models.CharField(max_length=200)
    userid = models.CharField(max_length=20)
    passwd = models.CharField(max_length=50)

