from django.db import models
import uuid

# Create your models here.

class SignatureImageUrl(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    signature = models.ImageField(upload_to='signatures')

class SignatureString(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    signature = models.TextField()
