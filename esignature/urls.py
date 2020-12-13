# Django
from django.urls import path
from django.conf import settings
from django.views.static import serve

# Own apps
import esignature
from . import views

urlpatterns = [
    path('media/signatures/<path>/', serve, {
        'document_root': settings.MEDIA_ROOT + '/signatures/'
    }),
    path('sign2image/', views.SignatureImageUrlCreateView.as_view(), name='signature_image_create_route'),
    path('sign2string/', views.SignatureStringCreateView.as_view(), name='signature_string_create_route'),
]
