
from app_memberprofilerole.mod_app.all_form_imports import *
from app_memberprofilerole.mod_member.models_member import *

class MemberorganizationroleForm(forms.ModelForm):
    class Meta:
        model = MemberOrganizationRole
        fields = ['member', 'org', 'role']
    def __init__(self, *args, **kwargs):
        super(MemberorganizationroleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

