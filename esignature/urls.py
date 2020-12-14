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
    path('sign-image/', views.SignatureImageUrlCreateView.as_view(), name='signature_image_create_route'),
    path('sign-string/', views.SignatureStringCreateView.as_view(), name='signature_string_create_route'),
    path('detail-string/<uuid:pk>/', views.SignatureStringDetailView.as_view(), name='signature_string_detail_route'),
    path('pdf-string/<uuid:pk>/', views.PdfStringDetailView.as_view(), name='pdf_string_detail_route'),
]
