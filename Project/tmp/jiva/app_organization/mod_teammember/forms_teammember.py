
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_teammember.models_teammember import *

class TeammemberForm(forms.ModelForm):
    class Meta:
        model = Teammember
        fields = ['member', 'member_role']
    def __init__(self, *args, **kwargs):
        super(TeammemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
