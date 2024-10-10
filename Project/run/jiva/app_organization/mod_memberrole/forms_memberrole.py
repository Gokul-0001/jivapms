
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_memberrole.models_memberrole import *

class MemberroleForm(forms.ModelForm):
    class Meta:
        model = Memberrole
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(MemberroleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

