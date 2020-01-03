from django import forms

from .models import Receipt, Food, Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs["class"] = "custom-file-input"
        self.fields['image'].widget.attrs["id"] = "receiptImg"

ImageCreateFormSet = forms.modelformset_factory(
    Image, form=ImageForm, extra=1
)
