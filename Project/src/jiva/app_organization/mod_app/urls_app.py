from django.urls import include, path

urlpatterns = [
    path('memberrole/', include('app_organization.mod_memberrole.urls_memberrole')),
    path('organization/', include('app_organization.mod_organization.urls_organization')),
    path('project/', include('app_organization.mod_project.urls_project')),
    path('team/', include('app_organization.mod_team.urls_team')),
    path('teammember/', include('app_organization.mod_teammember.urls_teammember')),
    path('work/', include('app_organization.mod_work.urls_work')),
]
