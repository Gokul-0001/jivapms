
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_persona.models_persona import *

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

