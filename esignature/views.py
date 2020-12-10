# Django
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Own apps
from .models import Signature
from .forms import SignatureForm


# Create your views here.
class SignatureCreateView(CreateView):
    model = Signature
    form_class = SignatureForm
    success_url = reverse_lazy('signature_create_route')
