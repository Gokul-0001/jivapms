
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_dev_value_stream.models_dev_value_stream import *
from app_organization.mod_app.all_view_imports import *
from app_memberprofilerole.mod_role.models_role import *
from app_memberprofilerole.mod_member.models_member import *
from app_organization.mod_project.models_project import *
from app_organization.mod_projectmembership.models_projectmembership import *
from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *

class DevValueStreamForm(forms.ModelForm):
    supporting_ops_steps = forms.ModelMultipleChoiceField(
        queryset=OpsValueStreamStep.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = DevValueStream
        fields = ['name', 'description', 'project', 'supporting_ops_steps']
    def __init__(self, *args, **kwargs):
        #super(DevValueStreamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
        user = kwargs.pop('user', None)  # Extract the user from kwargs
        org_id = kwargs.pop('org_id', None)  # Assuming org_id is passed to the form
        project_id = kwargs.pop('project_id', None)  # Assuming project_id 
        super(DevValueStreamForm, self).__init__(*args, **kwargs)
        
        # Fetch the member based on the user
        allowed_roles = [org_admin_str, project_admin_str]
        member = Member.objects.filter(user=user).first()
        allowed_roles_objs = Role.objects.filter(name__in=allowed_roles)
        # Fetch the organization
        organization = get_object_or_404(Organization, pk=org_id, active=True)
        # Check if the member has the Org Admin role
        has_org_admin_role = MemberOrganizationRole.objects.filter(
            member_id=member.id,
            org=organization,
            role__name=org_admin_str  # Check for Org Admin role by name
        ).exists()

        # Check if the member has the Project Admin role
        has_project_admin_role = MemberOrganizationRole.objects.filter(
            member_id=member.id,
            org=organization,
            role__name=project_admin_str  # Check for Project Admin role by name
        ).exists()
        print(f">>> === ORG MEMBERSHIP: OA:{has_org_admin_role}, PA:{has_project_admin_role} === <<< ")
        if has_org_admin_role:
            self.fields['project'].queryset = Project.objects.filter(org=organization)
        elif has_project_admin_role:
            # Filter projects where the member is assigned as a Project Admin
            TEST1 = Project.objects.filter(
                project_members__member=member,  # Links the Project to the member via Projectmembership
                project_members__project_role__role_type=PROJECT_ADMIN_ROLE_STR,  # Filter by Project Admin role type
                project_members__active=True  # Ensure the membership is active
            )
            self.fields['project'].queryset = TEST1
            print(f">>> === {TEST1} === <<<")
        else:
                # If the user is neither an Org Admin nor a Project Admin, no projects are available
                self.fields['project'].queryset = Project.objects.none()
                
        if org_id:
            self.fields['supporting_ops_steps'].queryset = OpsValueStreamStep.objects.filter(
                ops__org=organization,
                active=True,
            )