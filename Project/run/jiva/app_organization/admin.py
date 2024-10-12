from django.contrib import admin
from app_organization.mod_project.models_project import *
from app_organization.mod_projectmembership.models_projectmembership import *
from app_organization.mod_organization.models_organization import *
from app_organization.mod_organizationdetail.models_organizationdetail import *

class OrganizationDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'vision', 'mission', 'values', 'strategy', 'roadmap_description', 'created_at', 'updated_at')
admin.site.register(Organizationdetail, OrganizationDetailAdmin)



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
admin.site.register(Project, ProjectAdmin)

class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'project', 'project_role', 'created_at', 'updated_at')

admin.site.register(Projectmembership, ProjectMembershipAdmin)

class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = (  'role_type', 'description', 'created_at', 'updated_at')

admin.site.register(ProjectRole, ProjectRoleAdmin)

# Site related administration
class SiteOrgAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
admin.site.register(Organization, SiteOrgAdmin)
class SiteRoleAdmin(admin.ModelAdmin):
    list_display = ('role_type', 'description', 'created_at', 'updated_at')
admin.site.register(Siteorgrole, SiteRoleAdmin)
class SitemembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'org', 'org_role', 'created_at', 'updated_at')
admin.site.register(Sitemembership, SitemembershipAdmin)

# Register your models here.
