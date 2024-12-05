
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_impact_mapping.models_impact_mapping import *

class ImpactMapForm(forms.ModelForm):
    class Meta:
        model = ImpactMap
        fields = ['name', 'description', 'link_text']
    def __init__(self, *args, **kwargs):
        super(ImpactMapForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

