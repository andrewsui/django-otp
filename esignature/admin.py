from django.contrib import admin

from .models import SignatureImageUrl, SignatureString

# Register your models here.
admin.site.register(SignatureImageUrl)
admin.site.register(SignatureString)
