from django import forms
from .models import UploadedFile


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.original_name = self.cleaned_data['file'].name
        if commit:
            instance.save()
        return instance