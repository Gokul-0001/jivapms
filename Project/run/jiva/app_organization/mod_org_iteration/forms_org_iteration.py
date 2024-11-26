
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_org_iteration.models_org_iteration import *

class OrgIterationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="End Date"
    )
    iteration_length = forms.ChoiceField(
        choices=[
            ('0', '-- Select Iteration Length --'),
            ('0', 'Use Iteration Settings'),
            ('1', '1 Week'),
            ('2', '2 Weeks'),
            ('3', '3 Weeks'),
            ('4', '4 Weeks'),           
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Apply Release Iteration Length"
    )
    class Meta:
        model = OrgIteration
        fields = ['name', 'description', 'rel', 'start_date', 'end_date', 'iteration_length']
    def __init__(self, *args, **kwargs):
        super(OrgIterationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

