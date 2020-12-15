# Django
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# 3rd party

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


# PDF - WeasyPrint
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

class PdfWeasyPrintMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        DEFAULT_FILENAME = "document.pdf"

        # Render PDF
        html_template = render_to_string(self.template_name, context)
        pdf_file = HTML(string=html_template).write_pdf(
            # Load separate CSS stylesheet from static folder
            stylesheets=[CSS(settings.STATIC_ROOT + 'css/styles.css')]
        )
        response = HttpResponse(pdf_file, content_type='application/pdf')
        if hasattr(self, 'content_disposition'):
            response['Content-Disposition'] = self.content_disposition
        else:
            response['Content-Disposition'] = (
                'inline; filename=' + DEFAULT_FILENAME
            )
        return response

class PdfWeasyPrintDetailView(PdfWeasyPrintMixin, DetailView):
    model = SignatureString
    template_name = 'esignature/pdf_weasyprint_detail.html'
    # content_disposition = 'inline; filename="custom-filename.pdf"'


# PDF - xhtml2pdf
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa

class PdfXhtml2pdfMixin:
    '''
    To allow URL references to be resolved using Django’s STATIC_URL and
    MEDIA_URL settings, xhtml2pdf allows users to specify a link_callback
    parameter to point to a function that converts relative URLs to absolute
    system paths.
    '''
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access
        those resources.
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL      # e.g. /static/
            sRoot = settings.STATIC_ROOT    # e.g. /home/user/project_static/
            mUrl = settings.MEDIA_URL       # e.g. /media/
            mRoot = settings.MEDIA_ROOT     # e.g. /home/user/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # Make sure that file exists
        if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
        return path

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        DEFAULT_FILENAME = "document.pdf"

        # Create a Django response object, and specify content_type as PDF
        response = HttpResponse(content_type='application/pdf')
        if hasattr(self, 'content_disposition'):
            response['Content-Disposition'] = self.content_disposition
        else:
            response['Content-Disposition'] = (
                'inline; filename=' + DEFAULT_FILENAME
            )

        # Find the template and render it
        template = get_template(self.template_name)
        html = template.render(context)

        # Create a PDF
        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            link_callback=self.link_callback,
        )

        # If error then return error response
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        else:
            return response

class PdfXhtml2pdfDetailView(PdfXhtml2pdfMixin, DetailView):
    model = SignatureString
    template_name = 'esignature/pdf_xhtml2pdf_detail.html'
    # content_disposition = 'inline; filename="custom-filename.pdf"'
