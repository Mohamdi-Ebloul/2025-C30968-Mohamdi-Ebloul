from django import forms
from .models import Analysis

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif']


class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['image', 'notes']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'imageUpload',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Informations complémentaires (optionnel)...',
            }),
        }
        labels = {
            'image': 'Image médicale',
            'notes': 'Notes du médecin',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = image.name.split('.')[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    f"Format non supporté. Formats acceptés : {', '.join(ALLOWED_EXTENSIONS).upper()}"
                )
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("L'image ne doit pas dépasser 10 MB.")
        return image
