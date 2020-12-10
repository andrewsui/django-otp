# Django
from django.urls import path
from django.conf import settings
from django.views.static import serve

# Own apps
import esignature
from . import views

urlpatterns = [
    path('sign/', views.SignatureCreateView.as_view(), name='signature_create_route'),
    path('media/signatures/<path>/', serve, {
        'document_root': settings.MEDIA_ROOT + '/signatures/'
    }),
]
