# Django
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# 3rd party
from weasyprint import HTML, CSS

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

class SignatureStringDetailView(DetailView):
    model = SignatureString

class PdfMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # Render PDF
        html_template = render_to_string(self.template_name, context)
        pdf_file = HTML(string=html_template).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        if hasattr(self, 'content_disposition'):
            response['Content-Disposition'] = self.content_disposition
        else:
            response['Content-Disposition'] = 'inline; filename="report.pdf"'
        return response

class PdfStringDetailView(PdfMixin, DetailView):
    model = SignatureString
    template_name = 'esignature/pdfstring_detail.html'
    content_disposition = 'inline; filename="custom-filename.pdf"'
