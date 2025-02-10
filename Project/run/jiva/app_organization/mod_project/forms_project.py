
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project.models_project import *
from app_organization.mod_project_detail.models_project_detail import *
import pytz
import datetime
from django.utils.timezone import localtime
class ProjectForm(forms.ModelForm):
    # start_date = forms.DateField(required=False)
    # end_date = forms.DateField(required=False)
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
        fields = ['name', 'description',]
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
        local_tz = pytz.timezone('Asia/Kolkata')
        if self.instance.project_details.start_date:
            localized_start = localtime(self.instance.project_details.start_date, local_tz)
            self.fields['start_date'].initial = localized_start.date()
            print(f">>> Converted Start Date: {self.fields['start_date'].initial} <<<")  # Debugging

        if self.instance.project_details.end_date:
            localized_end = localtime(self.instance.project_details.end_date, local_tz)
            self.fields['end_date'].initial = localized_end.date()
            print(f">>> Converted End Date: {self.fields['end_date'].initial} <<<")  # Debugging

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        return start_date  # ✅ Return as a date (Django will store it as datetime)

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        return end_date  # ✅ Return as a date

    def save(self, commit=True):
        project = super().save(commit=False)
        if commit:
            project.save()
            project_detail, created = ProjectDetail.objects.get_or_create(pro=project)
            project_detail.start_date = self.cleaned_data['start_date']
            project_detail.end_date = self.cleaned_data['end_date']
            project_detail.save()
        return project