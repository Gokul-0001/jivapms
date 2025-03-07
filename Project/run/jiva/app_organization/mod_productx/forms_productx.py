
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_productx.models_productx import *

class ProductxForm(forms.ModelForm):
    class Meta:
        model = Productx
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProductxForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

