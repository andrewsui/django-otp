import base64
import uuid

from django import forms
from django.core.files.base import ContentFile
from django.utils.timezone import now

from .models import SignatureImageUrl, SignatureString

class SignatureImageUrlForm(forms.ModelForm):
    class Meta:
        model = SignatureImageUrl
        exclude = ['signature']
        signature = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['signature'] = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        base64_sig = cleaned_data.get('signature')
        if base64_sig==None:
            error_msg = "There was an issue uploading your signature. \
                Please try again."
            self.add_error('signature', error_msg)
        elif not base64_sig.startswith("data:image/png;base64,"):
            error_msg = "There was an issue uploading your signature. \
                Please try again."
            self.add_error('signature', error_msg)
        elif base64_sig == 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASw\
            AAACWCAYAAABkW7XSAAAAxUlEQVR4nO3BMQEAAADCoPVPbQhfoAAAAAAAAAAAAAAA\
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
                    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
                        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
                            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOA1\
                                v9QAATX68/0AAAAASUVORK5CYII=':
            error_msg = "Signature cannot be blank."
            self.add_error('signature', error_msg)
        else:
            data_format, img_str = base64_sig.split(';base64,') 
            ext = data_format.split('/')[-1]
            self.instance.signature = ContentFile(
                base64.b64decode(img_str),
                name = '{date_time}-{unique_ref}.{file_extension}'.format(
                    date_time = now().strftime('%Y%m%d-%H:%M'),
                    unique_ref = str(uuid.uuid4()),
                    file_extension = ext,
                )
            )
        return cleaned_data

class SignatureStringForm(forms.ModelForm):
    class Meta:
        model = SignatureString
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        base64_sig = cleaned_data.get('signature')
        if base64_sig==None:
            error_msg = "There was an issue uploading your signature. \
                Please try again."
            self.add_error('signature', error_msg)
        elif not base64_sig.startswith("data:image/png;base64,"):
            error_msg = "There was an issue uploading your signature. \
                Please try again."
            self.add_error('signature', error_msg)
        elif base64_sig == 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASw\
            AAACWCAYAAABkW7XSAAAAxUlEQVR4nO3BMQEAAADCoPVPbQhfoAAAAAAAAAAAAAAA\
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
                    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
                        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
                            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOA1\
                                v9QAATX68/0AAAAASUVORK5CYII=':
            error_msg = "Signature cannot be blank."
            self.add_error('signature', error_msg)
        else:
            return cleaned_data

