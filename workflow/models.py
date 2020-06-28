from django.db import models

# Create your models here.
from django.db import models
import uuid

class TempWork(models.Model):

    ticket_id = models.CharField(verbose_name="编号id", primary_key=True,max_length=200,default="111")
    #  该字段为主键

    process_recod = models.CharField('进度', max_length=2048)