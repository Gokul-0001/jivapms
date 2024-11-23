
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_image_map.models_image_map import *

class ImageMapForm(forms.ModelForm):
    class Meta:
        model = ImageMap
        fields = ['name', 'description', 'image', ]
    def __init__(self, *args, **kwargs):
        super(ImageMapForm, self).__init__(*args, **kwargs)
        
        # Custom widget for the image field
        if self.instance and self.instance.image:
            self.fields['image'].widget = forms.ClearableFileInput(attrs={
                'accept': 'image/*',  # Allows only images
                'style': 'max-width:100%; height:auto;',  # Prevents thumbnail constraint
            })
        
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("An image file is required.")
        return image
