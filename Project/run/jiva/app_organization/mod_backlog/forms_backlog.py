
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog_type.models_backlog_type import *
from app_organization.mod_backlog_super_type.models_backlog_super_type import *

from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_org_iteration.models_org_iteration import *

class BacklogSuperTypeForm(forms.ModelForm):
    class Meta:
        model = BacklogSuperType
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(BacklogSuperTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

class BacklogTypeForm(forms.ModelForm):
    class Meta:
        model = BacklogType
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(BacklogTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

class BacklogForm(forms.ModelForm):
    class Meta:
        model = Backlog
        fields = ['name', 'description', 'release', 'iteration', 'parent']

    def __init__(self, *args, **kwargs):
        super(BacklogForm, self).__init__(*args, **kwargs)

        # Filter releases to only active ones and add a placeholder
        self.fields['release'].queryset = OrgRelease.objects.filter(active=True)
        self.fields['release'].empty_label = '-- Select Release --'

        # Update the iteration queryset based on the selected release in POST data
        if 'release' in self.data:
            try:
                release_id = int(self.data.get('release'))
                self.fields['iteration'].queryset = OrgIteration.objects.filter(rel_id=release_id, active=True)
            except (ValueError, TypeError):
                self.fields['iteration'].queryset = OrgIteration.objects.none()
        elif 'release' in self.initial and self.initial['release']:
            release_id = self.initial['release']
            self.fields['iteration'].queryset = OrgIteration.objects.filter(rel_id=release_id, active=True)
        else:
            self.fields['iteration'].queryset = OrgIteration.objects.none()
        
        self.fields['iteration'].empty_label = '-- Select Iteration --'

        self.helper = FormHelper()
        self.helper.form_show_labels = False
