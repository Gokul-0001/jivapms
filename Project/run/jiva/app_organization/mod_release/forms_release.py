
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_release.models_release import *

class ReleaseForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Start Date"
    )
    release_length = forms.ChoiceField(
        choices=[
            ('', 'Select Length'),
            ('1', '1 Month'),
            ('2', '2 Months'),
            ('3', '3 Months'),
            ('4', '4 Months'),
            ('5', '5 Months'),
            ('6', '6 Months'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Release Length"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="End Date"
    )
    class Meta:
        model = Release
        fields = ['name', 'description', 'start_date', 'end_date', 'release_length']
    def __init__(self, *args, **kwargs):
        super(ReleaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

