from django.db import models

# Create your models here.

class FileManager(models.Model):
    file = models.ImageField()


class Document(models.Model):
    file_name = models.ForeignKey(FileManager, on_delete=models.CASCADE)
    approved_amount = models.BigIntegerField()
    extracted_amount = models.BigIntegerField()
    status = models.BooleanField(default=False)
