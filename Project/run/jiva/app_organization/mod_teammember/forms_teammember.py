
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_teammember.models_teammember import *
from app_organization.mod_memberrole.models_memberrole import *
# class TeammemberForm(forms.ModelForm):
#     class Meta:
#         model = Teammember
#         fields = ['member', 'member_role']
#     def __init__(self, *args, **kwargs):
#         super(TeammemberForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()  # Note: No need to pass 'self' here
#         self.helper.form_show_labels = False

class TeammemberForm(forms.ModelForm):
    class Meta:
        model = Teammember
        fields = ['member', 'member_role']
    
    def __init__(self, *args, **kwargs):
        # Assuming the team is passed via kwargs or can be accessed from the instance
        team = kwargs.pop('team', None)  # The team can be passed as a keyword argument
        
        super(TeammemberForm, self).__init__(*args, **kwargs)
        
        # Initialize crispy forms helper (if you're using crispy forms)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        # Filter member_role based on the team's organization
        if team:
            # Assuming team has a foreign key to Organization
            organization = team.org
            
            # Filter member_role based on the organization's roles
            self.fields['member_role'].queryset = Memberrole.objects.filter(org=organization)
        
        # Alternatively, if the instance exists and is related to a team, you can pull the team from the instance
        elif self.instance and self.instance.pk:
            organization = self.instance.team.org
            self.fields['member_role'].queryset = Memberrole.objects.filter(org=organization)
