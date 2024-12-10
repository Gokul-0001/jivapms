from app_organization.mod_project.models_project import *

from app_organization.mod_app.all_view_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.forms_backlog import *
from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_step.models_step import *
from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'backlog'
module_path = f'mod_backlog'


@login_required
def create_story_map(request, org_id):    
    projects = Organization.objects.get(pk=org_id).org_projects.filter(active=True)
    project = None 
    if request.method == 'POST':
        selected_project_id = request.POST.get('project')
        selected_story_map_option = request.POST.get('story_mapping_name')      
        project = Project.objects.get(pk=selected_project_id, active=True)
        #print(f"====> {selected_project_id} ===> {selected_story_map_option}")
        if selected_story_map_option == '2':
            return redirect('create_story_map_from_backlog', pro_id=selected_project_id)
        else:           
            # create a persona and send the persona id 
            new_persona = Persona.objects.create(name='', organization_id=org_id, project=project) 
            default_activity = Activity.objects.create(name='Default Activity', persona_id=new_persona.id)
            request.session['default_activity_id'] = default_activity.id
            #print(f">>> === DEFAULT ACTIVITY {default_activity.id} === <<<")
            return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=new_persona.id)
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_backlogs',
        'org_id': org_id,
        'projects': projects,
        'page_title': f'Backlog List',
    }       
    template_file = f"{app_name}/{module_path}/story_map/create_story_map.html"
    return render(request, template_file, context)

# @login_required
# def create_backlog_from_story_map(request, pro_id, persona_id):
#     pro = Project.objects.get(pk=pro_id)
#     persona = Persona.objects.get(pk=persona_id)
#     default_activity_id = request.session.pop('default_activity', None) 
#     organizaton = pro.org
#     releases = OrgRelease.objects.filter(org_id=pro.org_id, active=True)
#     activities = Activity.objects.filter(persona_id=persona_id, active=True)
#     backlog = Backlog.objects.filter(pro_id=pro_id, persona_id=persona_id, active=True) 
#     if request.method == 'POST':
#         if 'submit_activity' in request.POST:
#             selected_project_id = request.POST.get('project_id')
#             selected_persona_id = request.POST.get('persona_id')
#             activity_input = request.POST.get('activity')            
#             activity = Activity.objects.create(name=activity_input, persona_id=selected_persona_id)       
#             print(f">>> === ACTIVITY {activity} === <<<")     
#             return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=selected_persona_id)
#         if 'submit_detail' in request.POST:
#             selected_project_id = request.POST.get('project_id')
#             selected_persona_id = request.POST.get('persona_id')
#             detail_input = request.POST.get('detail')
#             detail = Backlog.objects.create(name=detail_input, persona_id=selected_persona_id, pro_id=selected_project_id)
#             print(f">>> === DETAIL {detail} === <<<")
#             return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=selected_persona_id)
    
#     # send outputs info, template,
#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'create_backlog_from_story_map',
#         'pro_id': pro_id,
#         'pro': pro,
#         'project': pro,
#         'persona_id': persona_id,
#         'persona': persona,
#         'activities': activities,
#         'default_activity_id': default_activity_id,
#         'backlog': backlog,
#         'releases': releases,
#         'org': pro.org,
#         'organization': pro.org,
#         'org_id': pro.org_id,
#         'page_title': f'Backlog from Story Map',
#     }       
#     template_file = f"{app_name}/{module_path}/story_map/create_backlog_from_story_map.html"
#     return render(request, template_file, context)

@login_required
def create_backlog_from_story_map(request, pro_id, persona_id):
    pro = get_object_or_404(Project, pk=pro_id)
    persona = get_object_or_404(Persona, pk=persona_id)
    default_activity_id = request.session.pop('default_activity', None)
    organization = pro.org
    releases = OrgRelease.objects.filter(org_id=pro.org_id, active=True)
    activities = Activity.objects.filter(persona_id=persona_id, active=True)
    backlog = Backlog.objects.filter(pro_id=pro_id, persona_id=persona_id, active=True)
    #StoryMapping.objects.all().delete()
    if request.method == 'POST':
        selected_project_id = request.POST.get('project_id')
        selected_persona_id = request.POST.get('persona_id')
        
        if 'submit_activity' in request.POST:
            activity_input = request.POST.get('activity')
            if activity_input:
                activity = Activity.objects.create(
                    name=activity_input,
                    persona_id=selected_persona_id,
                    project_id=selected_project_id,  # Ensure you link to the project if needed
                    active=True
                )
                print(f">>> === ACTIVITY {activity} === <<<")
            return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=selected_persona_id)
        
        elif 'submit_detail' in request.POST:
            detail_input = request.POST.get('detail')
            if detail_input:
                detail = Backlog.objects.create(
                    name=detail_input,
                    persona_id=selected_persona_id,
                    pro_id=selected_project_id,
                    active=True
                )
                print(f">>> === DETAIL {detail} === <<<")
            return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=selected_persona_id)
    
    # Context for GET request
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_backlog_from_story_map',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'persona_id': persona_id,
        'persona': persona,
        'activities': activities,
        'default_activity_id': default_activity_id,
        'backlog': backlog,
        'releases': releases,
        'org': organization,
        'organization': organization,
        'org_id': organization.id if organization else None,
        'page_title': 'Backlog from Story Map',
    }
    
    template_file = f"{app_name}/{module_path}/story_map/create_backlog_from_story_map.html"
    return render(request, template_file, context)

@login_required
def create_story_map_from_backlog(request, pro_id):    
    pro = Project.objects.get(pk=pro_id)
    organization = pro.org
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_story_map_from_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'organization': pro.org,
        'org_id': pro.org_id,
        'page_title': f'Story Map from Backlog',
    }       
    template_file = f"{app_name}/{module_path}/story_map/create_story_map_from_backlog.html"
    return render(request, template_file, context)


# ajax
@login_required
def ajax_storymap_right_pane_content(request):
    if request.method == 'POST':
        user = request.user
        pro_id = request.POST.get('pro_id')
        pro = Project.objects.get(pk=pro_id)
        persona_id = request.POST.get('persona_id')
        persona = Persona.objects.get(pk=persona_id)
        default_activity_id = request.session.get('default_activity_id')
        organization = pro.org
        
        activities = Activity.objects.filter(active=True, persona=persona)  # Fetch activities
        releases = OrgRelease.objects.filter(active=True, org=organization)  # Fetch releases
        # send outputs info, template,
        context = {
            'parent_page': '___PARENTPAGE___',
            'page': 'create_story_map_from_backlog',
            'pro_id': pro_id,
            'pro': pro,
            'project': pro,
            'org': pro.org,
            'organization': pro.org,
            'default_activity_id': default_activity_id,
            'activities': activities,
            'releases': releases,
            'org_id': pro.org_id,
            'page_title': f'Story Map from Backlog',
        }       
        template_file = f"{app_name}/{module_path}/story_map/ajax_storymap_right_pane_content.html"
        
        html_content = render_to_string(template_file, context)
        #print(f">>> === {html_content} === <<<")
        return JsonResponse({'html': html_content})

    return JsonResponse({'error': 'true', 'message': 'Invalid Request: Use POST method.'})    



@login_required
def ajax_storymap_refresh_steps_row(request):
    if request.method == 'POST':
        user = request.user
        pro_id = request.POST.get('pro_id')
        pro = Project.objects.get(pk=pro_id)
        persona_id = request.POST.get('persona_id')
        persona = Persona.objects.get(pk=persona_id)
        organization = pro.org
        # Fetch the required data
        activities = Activity.objects.filter(active=True, persona_id=persona_id).prefetch_related('activity_steps')
        # context
        context = {
            'activities': activities,
            'persona': persona,
            'pro': pro,
            'organization': organization,
            'org_id': organization.id,
            'pro_id': pro_id,
            'persona_id': persona_id,
        }
        # Render the partial HTML
        template_file = f"{app_name}/{module_path}/story_map/partial_steps_row.html"
        steps_html = render_to_string(template_file, context)
    
        return JsonResponse({"status": "success", "html": steps_html})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)