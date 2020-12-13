# Django
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Own apps
from .models import SignatureImageUrl, SignatureString
from .forms import SignatureImageUrlForm, SignatureStringForm


# Create your views here.
class SignatureImageUrlCreateView(CreateView):
    model = SignatureImageUrl
    form_class = SignatureImageUrlForm
    template_name = 'esignature/signature_form.html'
    success_url = reverse_lazy('signature_image_create_route')

class SignatureStringCreateView(CreateView):
    model = SignatureString
    form_class = SignatureStringForm
    template_name = 'esignature/signature_form.html'
    success_url = reverse_lazy('signature_string_create_route')
