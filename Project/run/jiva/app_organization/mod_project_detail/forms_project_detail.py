
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_detail.models_project_detail import *

from app_organization.mod_project_template.models_project_template import *

class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        fields = ['vision', 'mission', 'values', 'strategy', 'roadmap_description', 'template'
                  ,'start_date', 'end_date']
    def __init__(self, *args, **kwargs):
        super(ProjectDetailForm, self).__init__(*args, **kwargs)
        
        # Filter templates where active=True
        self.fields['template'].queryset = ProjectTemplate.objects.filter(active=True)
        
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

