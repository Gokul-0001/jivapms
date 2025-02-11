from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project.models_project import *
from app_organization.mod_project_detail.models_project_detail import *
import pytz
import datetime
from django.utils.timezone import localtime

class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width: auto; max-width: 150px;'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width: auto; max-width: 150px;'})
    )

    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        local_tz = pytz.timezone('Asia/Kolkata')

        # Check if instance exists and has an ID (i.e., it's being edited)
        if self.instance.pk:
            project_details = getattr(self.instance, 'project_details', None)  # Safe retrieval

            if project_details and project_details.start_date:
                localized_start = localtime(project_details.start_date, local_tz)
                self.fields['start_date'].initial = localized_start.date()

            if project_details and project_details.end_date:
                localized_end = localtime(project_details.end_date, local_tz)
                self.fields['end_date'].initial = localized_end.date()

    def clean_start_date(self):
        return self.cleaned_data.get('start_date')

    def clean_end_date(self):
        return self.cleaned_data.get('end_date')

    def save(self, commit=True):
        project = super().save(commit=False)
        
        if commit:
            project.save()
            
            # Ensure ProjectDetail exists before updating
            project_detail, created = ProjectDetail.objects.get_or_create(pro=project)

            # Only update dates if provided
            if 'start_date' in self.cleaned_data and self.cleaned_data['start_date']:
                project_detail.start_date = self.cleaned_data['start_date']
            if 'end_date' in self.cleaned_data and self.cleaned_data['end_date']:
                project_detail.end_date = self.cleaned_data['end_date']
            
            project_detail.save()
        
        return project
