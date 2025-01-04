
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_org_release.models_org_release import *


class OrgReleaseBasicForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="End Date"
    )
    release_length = forms.ChoiceField(
        choices=[
            ('', '-- Select Length --'),
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
    
    apply_release_iteration_length = forms.ChoiceField(
        choices=[
            ('', '-- Select Iteration Length --'),
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
        model = OrgRelease
        fields = ['name', 'description', 'start_date', 'end_date', 'release_length', 'apply_release_iteration_length']
    def __init__(self, *args, **kwargs):
        super(OrgReleaseBasicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False




class OrgReleaseForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="End Date"
    )
    release_length = forms.ChoiceField(
        choices=[
            ('', '-- Select Length --'),
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
    
    apply_release_iteration_length = forms.ChoiceField(
        choices=[
            ('', '-- Select Iteration Length --'),
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
        model = OrgRelease
        fields = ['name', 'description', 'start_date', 'end_date', 'release_length', 'apply_release_iteration_length', 'no_of_iterations']
    def __init__(self, *args, **kwargs):
        super(OrgReleaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False




from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class OrgReleaseWithTimeForm(forms.ModelForm):
    # Use DateTimeField with the correct format and input widget
    release_start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        label="Start Date-Time",
        input_formats=['%Y-%m-%dT%H:%M']  # Matches 'datetime-local' input
    )
    release_end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        label="End Date-Time",
        input_formats=['%Y-%m-%dT%H:%M']  # Matches 'datetime-local' input
    )

    class Meta:
        model = OrgRelease
        fields = [
            'name',
            'description',
            'release_start_date',
            'release_end_date',
            'release_length_in_mins',
            'iteration_length_in_mins'
        ]

    def __init__(self, *args, **kwargs):
        super(OrgReleaseWithTimeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'name',
            'description',
            'release_start_date',
            'release_length_in_mins',
            'iteration_length_in_mins',
            'release_end_date',
            Submit('submit', 'Save')
        )
