from django.urls import include, path

urlpatterns = [
    path('member/', include('app_memberprofilerole.mod_member.urls_member')),
    path('memberorganizationrole/', include('app_memberprofilerole.mod_memberorganizationrole.urls_memberorganizationrole')),
    path('profile/', include('app_memberprofilerole.mod_profile.urls_profile')),
    path('regcode/', include('app_memberprofilerole.mod_regcode.urls_regcode')),
    path('role/', include('app_memberprofilerole.mod_role.urls_role')),
]
