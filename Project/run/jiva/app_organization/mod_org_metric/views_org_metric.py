
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_org_metric.models_org_metric import *
from app_organization.mod_org_metric.forms_org_metric import *

from app_organization.mod_organization.models_organization import *
from app_organization.mod_project.models_project import *

from app_common.mod_app.all_view_imports import *
from app_common.mod_common.models_common import *

from app_jivapms.mod_web.views_web import *
from app_common.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'org_metrics'
module_path = f'mod_org_metric'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list_org_metrics(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgMetric.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgMetric.objects.filter(active=True, org_id=org_id).order_by('position')
        deleted = OrgMetric.objects.filter(active=False, deleted=False,
                                org_id=org_id,
                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
             
        if 'selected_item' in request.POST:  # Correct the typo here
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  # Ensure item_id is converted to int if necessary
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(OrgMetric, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OrgMetric, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OrgMetric, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OrgMetric, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_org_metrics', org_id=org_id)
            return redirect('list_org_metrics', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_org_metrics',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Org_metric List',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }       
    template_file = f"{app_name}/{module_path}/list_org_metrics.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_org_metrics(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgMetric.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgMetric.objects.filter(active=False, deleted=False, org_id=org_id,
                                            **viewable_dict).order_by('position')        
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
     
        if 'selected_item' in request.POST:  # Correct the typo here
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  # Ensure item_id is converted to int if necessary
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(OrgMetric, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OrgMetric, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_org_metrics', org_id=org_id)
                redirect('list_org_metrics', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_org_metrics',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Org_metric List',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_org_metrics.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_org_metric(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = OrgMetricForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_metrics', org_id=org_id)
    else:
        form = OrgMetricForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/create_org_metric.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_org_metric(request, org_id, org_metric_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OrgMetricForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_metrics', org_id=org_id)
    else:
        form = OrgMetricForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/edit_org_metric.html"
    return render(request, template_file, context)



@login_required
def delete_org_metric(request, org_id, org_metric_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_org_metrics', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/delete_org_metric.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_org_metric(request, org_id, org_metric_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_org_metrics', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_org_metric.html"
    return render(request, template_file, context)


@login_required
def restore_org_metric(request,  org_id, org_metric_id):
    user = request.user
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_org_metrics', org_id=org_id)
   


@login_required
def view_org_metric(request, org_id, org_metric_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/view_org_metric.html"
    return render(request, template_file, context)


from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.views_project_tree import jivapms_mod_backlog_helper_get_backlog_details
# @login_required
# def view_project_metrics(request, project_id):
#     user = request.user
#     project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
#     organization = project.org
#     org_id = organization.id
    
#     # get the backlog details
#     backlog_details = jivapms_mod_backlog_helper_get_backlog_details(request, project_id)
#     include_types = backlog_details['include_types']
    
#     end_date = now().date()  # Today's date
#     start_date = end_date - timedelta(days=90)  # Last 3 months
#     logger.debug(f">>> === start_date: {start_date} === <<<")
#     logger.debug(f">>> === end_date: {end_date} === <<<")

#     # Query backlog data
#     backlog_check = Backlog.objects.filter(pro=project, active=True, deleted=False, type__in=include_types)
#     backlog_count = backlog_check.count()
#     logger.debug(f">>> === backlog_count: {backlog_count} === <<<")
    
    
#     backlog_data = (
#         Backlog.objects
#         .filter(pro=project, created_at__range=(start_date, end_date), active=True, deleted=False, type__in=include_types)
#         .extra({'created_date': "date(created_at)"})
#         .values('created_date', 'status')
#         .annotate(count=models.Count('id'))
#         .order_by('created_date')
#     )

#     # Prepare data for Chart.js
#     labels = [item['created_date'] for item in backlog_data]
#     daily_counts = [item['count'] for item in backlog_data]

#     # Compute cumulative counts
#     cumulative_counts = []
#     total = 0
#     for count in daily_counts:
#         total += count
#         cumulative_counts.append(total)

#     # Prepare data for Chart.js
#     labels = []
#     daily_counts = []
#     cumulative_counts = []
#     to_do_counts = []
#     in_progress_counts = []
#     done_counts = []
#     backlog_counts = []
    
#     total_count = 0
#     to_do_total = 0
#     in_progress_total = 0
#     done_total = 0
#     backlog_total = 0

#     for item in backlog_data:
#         labels.append(item['created_date'])
#         daily_counts.append(item['count'])

#         # Calculate cumulative counts
#         total_count += item['count']
#         cumulative_counts.append(total_count)

#         # Calculate cumulative counts for each status
#         if item['status'] == 'To Do':
#             to_do_total += item['count']
#         elif item['status'] == 'In Progress':
#             in_progress_total += item['count']
#         elif item['status'] == 'Done':
#             done_total += item['count']

#         # Calculate the total backlog count as the sum of all statuses
#         backlog_total = to_do_total + in_progress_total + done_total
        
#         logger.debug(f">>> === backlog_total: {backlog_total} === <<<")
#         logger.debug(f">>> === to_do_total: {to_do_total} === <<<")
#         logger.debug(f">>> === in_progress_total: {in_progress_total} === <<<")
#         logger.debug(f">>> === done_total: {done_total} === <<<")
        

#         # Append CFD data
#         backlog_counts.append(backlog_total)
#         to_do_counts.append(to_do_total)
#         in_progress_counts.append(in_progress_total)
#         done_counts.append(done_total)

       


#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'view_project_metrics',
#         'organization': organization,
#         'org_id': org_id,
        
#         'module_path': module_path,
        
#         'page_title': f'View Project Metrics',
#         'labels': labels,
#         'data': daily_counts,
#         'cumulative_data': cumulative_counts,
#         'to_do_data': to_do_counts,          # To Do status counts
#         'in_progress_data': in_progress_counts,  # In Progress status counts
#         'done_data': done_counts,          # Done status counts
#         'backlog_data': backlog_counts,    # Backlog status counts
#         'project': project,
#         'project_id': project_id,
#         'pro_id': project_id,
#     }
    
#     template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics.html"
#     return render(request, template_file, context)

# === testing
# @login_required
# def view_project_metrics(request, project_id):
#     user = request.user
#     project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
#     organization = project.org
#     org_id = organization.id
    
#     # get the backlog details
#     backlog_details = jivapms_mod_backlog_helper_get_backlog_details(request, project_id)
#     include_types = backlog_details['include_types']
    
#     # Date range
#     end_date = now().date()  # Today's date
#     start_date = end_date - timedelta(days=90)  # Last 3 months
#     logger.debug(f">>> === start_date: {start_date} === <<<")
#     logger.debug(f">>> === end_date: {end_date} === <<<")

#     # Query backlog data
#     backlog_check = Backlog.objects.filter(pro=project, active=True, deleted=False, type__in=include_types)
#     backlog_count = backlog_check.count()
#     logger.debug(f">>> === backlog_count: {backlog_count} === <<<")
    
    
#     backlog_data = (
#         Backlog.objects
#         .filter(pro=project, created_at__range=(start_date, end_date), active=True, deleted=False, type__in=include_types)
#         .extra({'created_date': "date(created_at)"})
#         .values('created_date', 'status')
#         .annotate(count=models.Count('id'))
#         .order_by('created_date')
#     )

#     # Prepare data for Chart.js
#     labels = []
#     daily_counts = []
#     cumulative_counts = []
#     to_do_counts = []
#     in_progress_counts = []
#     done_counts = []
#     backlog_counts = []
    
#     # Initialize counters
#     total_count = 0
#     to_do_total = 0
#     in_progress_total = 0
#     done_total = 0
#     backlog_total = 0

#     # Process each entry in backlog data
#     for item in backlog_data:
#         labels.append(item['created_date'])
#         daily_counts.append(item['count'])

#         # Calculate cumulative counts
#         total_count += item['count']
#         cumulative_counts.append(total_count)

#         # Calculate cumulative counts for each status
#         if item['status'] == 'To Do' or item['status'] == 'To Do':
#             to_do_total += item['count']
#         elif item['status'] == 'WIP':
#             in_progress_total += item['count']
#         elif item['status'] == 'Done':
#             done_total += item['count']

#         # Calculate the total backlog count as the sum of all statuses
#         backlog_total = to_do_total + in_progress_total + done_total
        
#         # Debugging logs for verification
#         logger.debug(
#             f">>> === Date: {item['created_date']} | "
#             f"Status: {item['status']} | "
#             f"Daily Count: {item['count']} | "
#             f"Backlog Total: {backlog_total} | "
#             f"To Do: {to_do_total} | "
#             f"In Progress: {in_progress_total} | "
#             f"Done: {done_total} | "
#             f"Cumulative Total: {total_count} === <<<"
#         )
        
#         # Append CFD data
#         backlog_counts.append(backlog_total)
#         to_do_counts.append(to_do_total)
#         in_progress_counts.append(in_progress_total)
#         done_counts.append(done_total)

#     # Context for rendering
#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'view_project_metrics',
#         'organization': organization,
#         'org_id': org_id,
        
#         'module_path': module_path,
        
#         'page_title': f'View Project Metrics',
#         'labels': labels,
#         'data': daily_counts,
#         'cumulative_data': cumulative_counts,
#         'to_do_data': to_do_counts,          # To Do status counts
#         'in_progress_data': in_progress_counts,  # In Progress status counts
#         'done_data': done_counts,          # Done status counts
#         'backlog_data': backlog_counts,    # Backlog status counts
#         'project': project,
#         'project_id': project_id,
#         'pro_id': project_id,
#     }
    
#     template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics.html"
#     return render(request, template_file, context)

from django.db.models.functions import TruncDate

from app_organization.mod_org_board.models_org_board import *


# @login_required
# def view_project_metrics(request, project_id):
#     # Fetch user, project, and organization details
#     user = request.user
#     project = get_object_or_404(Project, pk=project_id, active=True)
#     organization = project.org
#     org_id = organization.id

#     # Get backlog details
#     backlog_details = jivapms_mod_backlog_helper_get_backlog_details(request, project_id)
#     include_types = backlog_details['include_types']

#     # Date range for the last 90 days
#     end_date = now().date()
#     start_date = end_date - timedelta(days=90)

#     # Initialize variables
#     date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
#     to_do_counts = {date: 0 for date in date_range}
#     wip_counts = {date: 0 for date in date_range}
#     done_counts = {date: 0 for date in date_range}
#     backlog_counts = {date: 0 for date in date_range}

#     # Fetch initial backlog data (card creation counts)
#     backlog_data = (
#         Backlog.objects.filter(
#             pro=project,
#             created_at__range=(start_date, end_date),
#             active=True,
#             deleted=False,
#             type__in=include_types
#         )
#         .annotate(date_created=TruncDate('created_at'))
#         .values('date_created', 'status')
#         .annotate(count=Count('id'))
#         .order_by('date_created')
#     )

#     # Process backlog data
#     for item in backlog_data:
#         created_date = item['date_created']
#         status = item['status']
#         count = item['count']

#         # Add initial counts based on status
#         if status == 'To Do':
#             to_do_counts[created_date] += count
#         elif status == 'WIP':
#             wip_counts[created_date] += count
#         elif status == 'Done':
#             done_counts[created_date] += count

#         # Total backlog count (initial state)
#         backlog_counts[created_date] += count

#     # Fetch transition data (state movements)
#     transitions = (
#         ProjectBoardStateTransition.objects.filter(
#             card__pro=project,
#             transition_time__date__range=(start_date, end_date)
#         )
#         .annotate(date=TruncDate('transition_time'))
#         .values('date', 'from_state__name', 'to_state__name')
#         .annotate(count=Count('id'))
#     )

#     # Process transitions
#     for transition in transitions:
#         date = transition['date']
#         from_state = transition['from_state__name']
#         to_state = transition['to_state__name']
#         count = transition['count']

#         # Subtract from the previous state
#         if from_state == 'To Do':
#             to_do_counts[date] -= count
#         elif from_state == 'WIP':
#             wip_counts[date] -= count
#         elif from_state == 'Done':
#             done_counts[date] -= count

#         # Add to the new state
#         if to_state == 'To Do':
#             to_do_counts[date] += count
#         elif to_state == 'WIP':
#             wip_counts[date] += count
#         elif to_state == 'Done':
#             done_counts[date] += count

#     # Cumulative counters
#     cumulative_to_do = []
#     cumulative_wip = []
#     cumulative_done = []
#     cumulative_total = []
#     cumulative_counts = []
#     labels = []
#     daily_counts = []

#     running_to_do = 0
#     running_wip = 0
#     running_done = 0
#     running_total = 0

#     # Generate cumulative data for CFD
#     for date in date_range:
#         labels.append(date.strftime('%Y-%m-%d'))
#         running_to_do += to_do_counts[date]
#         running_wip += wip_counts[date]
#         running_done += done_counts[date]
#         running_total += backlog_counts[date]

#         cumulative_to_do.append(running_to_do)
#         cumulative_wip.append(running_wip)
#         cumulative_done.append(running_done)
#         cumulative_total.append(running_total)
#         cumulative_counts.append(running_total)
#         daily_counts.append(backlog_counts[date])

#     # Debugging logs
#     logger.debug(f"Labels: {labels}")
#     logger.debug(f"To Do: {cumulative_to_do}")
#     logger.debug(f"WIP: {cumulative_wip}")
#     logger.debug(f"Done: {cumulative_done}")
#     logger.debug(f"Total: {cumulative_total}")

#     # Prepare context for rendering template
#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'view_project_metrics',
#         'organization': organization,
#         'org_id': org_id,
#         'project': project,
#         'project_id': project_id,
#         'pro_id': project_id,

#         # Chart Data for CFD
#         'labels': labels,                      # X-axis labels (dates)
#         'data': daily_counts,                  # Daily backlog counts
#         'cumulative_data': cumulative_counts,  # Total cumulative counts
#         'to_do_data': cumulative_to_do,        # To Do cumulative counts
#         'in_progress_data': cumulative_wip,    # WIP cumulative counts
#         'done_data': cumulative_done,          # Done cumulative counts
#         'backlog_data': list(backlog_counts.values()),  # Backlog counts
#     }

#     # Render template
#     template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics.html"
#     return render(request, template_file, context)


@login_required
def view_project_metrics(request, project_id):
    from datetime import timedelta, date
    import random
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics',
        'organization': project.org,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,

        
    }

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics.html"
    return render(request, template_file, context)


@login_required
def view_project_metrics_iteration_tab(request, project_id):
    # Fetch user, project, and organization details
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    iteration_backlog_items = None
    logger.debug(f">>> === project: {project} {project.project_release} === <<<")
 
    
    # Project Release and Iteration
    current_release = None
    current_iteration = None
    current_datetime = now().replace(microsecond=0)
    release_mismatch_flag = False
    iteration_mismatch_flag = False
    # Step 1: Check Project Release
    if project.project_release:
       # Filter by date and time separately
        current_release = OrgRelease.objects.filter(
            id=project.project_release.id,
            release_start_date__lte=current_datetime,
            release_end_date__gte=current_datetime,            
        ).order_by("-release_start_date").first()      
        if current_release:
            logger.debug(f">>> === current_release: {current_release} {current_release.release_start_date} === <<<")
        else:
            release_mismatch_flag = True
    # Step 2: Check Project Iteration
    total_story_points = 0
    todo_story_points = 0
    wip_story_points = 0
    done_story_points = 0
    if project.project_iteration:
        # Use datetime comparison for both start and end dates
        current_datetime = now().replace(microsecond=0)
        details = get_project_release_and_iteration_details(project.id)
        current_release = details['current_release']
        current_iteration = details['current_iteration']
        next_iteration = details['next_iteration']       
        

        if current_iteration:
            logger.debug(f">>> === current_iteration: {current_iteration} {current_iteration.iteration_start_date} === <<<")

            # Filter backlog items for the current iteration
            iteration_backlog_items = Backlog.objects.filter(
                pro=project, 
                active=True, 
                deleted=False, 
                iteration=current_iteration
            )
            logger.debug(f">>> === iteration_backlog_items: {iteration_backlog_items} === <<<")

            # Calculate total story points
            total_story_points = iteration_backlog_items.aggregate(total=Sum('size'))['total'] or 0
            # CHECK THE PROJECT BOARD CARD details MODEL
            project_board = ProjectBoard.objects.filter(project=project, org_release=current_release, org_iteration=current_iteration, active=True).first()
            logger.debug(f">>> === project_board: {project_board} === <<<")
            
            
            # # Calculate story points by status
            # todo_story_points = iteration_backlog_items.filter(status="ToDo").aggregate(total=Sum('size'))['total'] or 0
            # wip_story_points = iteration_backlog_items.filter(status="WIP").aggregate(total=Sum('size'))['total'] or 0
            # done_story_points = iteration_backlog_items.filter(status="Done").aggregate(total=Sum('size'))['total'] or 0
            # Fetch the states for each status from ProjectBoardCardState
            # Fetch the states for ToDo, WIP, and Done from ProjectBoardState
           
            # Fetch states by their names
            todo_states = ProjectBoardState.objects.filter(name="ToDo", active=True).values_list('id', flat=True)
            wip_states = ProjectBoardState.objects.filter(name="WIP", active=True).values_list('id', flat=True)
            done_states = ProjectBoardState.objects.filter(name="Done", active=True).values_list('id', flat=True)

            logger.debug(f"ToDo States: {list(todo_states)}")
            logger.debug(f"WIP States: {list(wip_states)}")
            logger.debug(f"Done States: {list(done_states)}")

            # Fetch ProjectBoardCards linked to these states
            todo_cards_objects = ProjectBoardCard.objects.filter(board=project_board, state_id__in=todo_states, active=True)
            wip_cards_objects = ProjectBoardCard.objects.filter(board=project_board, state_id__in=wip_states, active=True)
            done_cards_objects = ProjectBoardCard.objects.filter(board=project_board, state_id__in=done_states, active=True)

            # Log card counts and details
            logger.debug(f"ToDo Cards Count: {todo_cards_objects.count()}")
            logger.debug(f"WIP Cards Count: {wip_cards_objects.count()}")
            logger.debug(f"Done Cards Count: {done_cards_objects.count()}")

            # Extract backlog IDs from cards
            todo_cards = todo_cards_objects.values_list('backlog_id', flat=True)
            wip_cards = wip_cards_objects.values_list('backlog_id', flat=True)
            done_cards = done_cards_objects.values_list('backlog_id', flat=True)

            logger.debug(f"ToDo Backlog IDs: {list(todo_cards)}")
            logger.debug(f"WIP Backlog IDs: {list(wip_cards)}")
            logger.debug(f"Done Backlog IDs: {list(done_cards)}")

            # Verify matching backlog items
            todo_items = iteration_backlog_items.filter(id__in=todo_cards)
            wip_items = iteration_backlog_items.filter(id__in=wip_cards)
            done_items = iteration_backlog_items.filter(id__in=done_cards)

            logger.debug(f"ToDo Items Count: {todo_items.count()}")
            logger.debug(f"WIP Items Count: {wip_items.count()}")
            logger.debug(f"Done Items Count: {done_items.count()}")

            # Helper function to calculate numeric story points
            def get_numeric_story_points(backlog_items):
                total_points = 0
                for item in backlog_items:
                    size = item.size
                    # Check if size is numeric or a valid integer-like string
                    if isinstance(size, (int, float)):
                        total_points += size
                    elif isinstance(size, str):
                        size = size.strip()
                        if size.isdigit():
                            total_points += int(size)
                        else:
                            logger.warning(f"Invalid size value: {size}")
                    else:
                        logger.warning(f"Unsupported size type: {type(size)}")
                return total_points

            # Calculate story points using the helper function
            todo_story_points = get_numeric_story_points(todo_items)
            wip_story_points = get_numeric_story_points(wip_items)
            done_story_points = get_numeric_story_points(done_items)

            logger.debug(f"ToDo Story Points: {todo_story_points}")
            logger.debug(f"WIP Story Points: {wip_story_points}")
            logger.debug(f"Done Story Points: {done_story_points}")

        
            # Log the results
            logger.debug(f"Total Story Points: {total_story_points}")
            logger.debug(f"ToDo Story Points: {todo_story_points}")
            logger.debug(f"WIP Story Points: {wip_story_points}")
            logger.debug(f"Done Story Points: {done_story_points}")
            
            
           
            
        else:
            iteration_mismatch_flag = True

    # Set the Iteration backlog items count
    iteration_backlog_items_count = iteration_backlog_items.count() if iteration_backlog_items else 0
    
    
    ##
    ##
    ## BURNDOWN CHART
    ##
    ##

    from datetime import timedelta

    # Prepare Burndown Chart Data
    if current_iteration:
        logger.debug(f">>> === BURNDOWNcurrent_iteration: {current_iteration} === <<<")
        iteration_start_date = current_iteration.iteration_start_date
        iteration_end_date = current_iteration.iteration_end_date
        
        # Create date range
        days_range = (iteration_end_date - iteration_start_date).days + 1
        burndown_data = []
        current_date = now().date()
        for i in range(days_range):
            itr_date = iteration_start_date + timedelta(days=i)  # Correct usage of timedelta
            
           # Filter backlog items for the current iteration
            backlog_items = Backlog.objects.filter(
                pro=project, 
                active=True, 
                iteration=current_iteration,
                done_at__date__lte=itr_date
            )
            
            # Log each done_at value and current_date
            for item in backlog_items:
                logger.debug(f"CHECK Backlog ID: {item.id}, {item}, done_at: {item.done_at}, current_date: {itr_date}")
            
            # Calculate remaining story points for each date
            done_story_points_till_date = backlog_items.aggregate(total=Sum('size'))['total'] or 0
            remaining_story_points = total_story_points - done_story_points_till_date
            logger.debug(f">>> === itr_date: {itr_date} | done_story_points_till_date: {done_story_points_till_date} | remaining_story_points: {remaining_story_points} === <<<")
            if itr_date.date() > current_date:
                remaining_story_points = ''
            burndown_data.append({
            'date': itr_date.strftime('%Y-%m-%d'),
            'remaining_story_points': remaining_story_points
            })
            
        # Log the complete burndown data
        logger.debug(f">>> === burndown_data: {burndown_data} === <<<")

           
    
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_iteration_tab',
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
        'current_release': current_release,
        'current_iteration': current_iteration,
        'release_mismatch_flag': release_mismatch_flag,
        'iteration_mismatch_flag': iteration_mismatch_flag,
        'iteration_backlog_items': iteration_backlog_items,
        'iteration_backlog_items_count': iteration_backlog_items_count,
        'total_story_points': total_story_points,
        'todo_story_points': todo_story_points,
        'wip_story_points': wip_story_points,
        'done_story_points': done_story_points,
        
        'burndown_data': burndown_data,
    }

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics_iteration_tab.html"
    return render(request, template_file, context)


@login_required
def view_project_metrics_quality_tab(request, project_id):
    # Fetch user, project, and organization details
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_quality_tab',
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,

    }

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics_quality_tab.html"
    return render(request, template_file, context)







    # release_start_date = current_release.release_start_date.replace(microsecond=0)
        # release_end_date = current_release.release_end_date.replace(microsecond=0)
        # logger.debug(f">>> === current_datetime: {current_datetime} === <<<")
        # logger.debug(f">>> === release_start_date: {release_start_date} === <<<")
        # logger.debug(f">>> === release_end_date: {release_end_date} === <<<")
        # if release_start_date <= current_datetime <= release_end_date:
        #     logger.debug(f">>> === Current datetime {current_datetime} is within the release period {release_start_date}--{release_end_date}. === <<<")
        # else:
        #     logger.debug(f">>> === Current datetime is outside the release period. === <<<")
        
        
        
        
##
##
## reference 1701
##
##



    # from datetime import timedelta

    # # Prepare Burndown Chart Data
    # if current_iteration:
    #     logger.debug(f">>> === BURNDOWNcurrent_iteration: {current_iteration} === <<<")
    #     iteration_start_date = current_iteration.iteration_start_date
    #     iteration_end_date = current_iteration.iteration_end_date
        
    #     # Create date range
    #     days_range = (iteration_end_date - iteration_start_date).days + 1
    #     burndown_data = []
    #     current_date = now().date()
    #     for i in range(days_range):
    #         itr_date = iteration_start_date + timedelta(days=i)  # Correct usage of timedelta
            
    #        # Filter backlog items for the current iteration
    #         backlog_items = Backlog.objects.filter(
    #             pro=project, 
    #             active=True, 
    #             iteration=current_iteration,
    #             done_at__date__lte=itr_date
    #         )
            
    #         # Log each done_at value and current_date
    #         for item in backlog_items:
    #             logger.debug(f"CHECK Backlog ID: {item.id}, {item}, done_at: {item.done_at}, current_date: {itr_date}")
            
    #         # Calculate remaining story points for each date
    #         done_story_points_till_date = backlog_items.aggregate(total=Sum('size'))['total'] or 0
    #         remaining_story_points = total_story_points - done_story_points_till_date
    #         logger.debug(f">>> === itr_date: {itr_date} | done_story_points_till_date: {done_story_points_till_date} | remaining_story_points: {remaining_story_points} === <<<")
    #         if itr_date.date() > current_date:
    #             remaining_story_points = ''
    #         burndown_data.append({
    #         'date': itr_date.strftime('%Y-%m-%d'),
    #         'remaining_story_points': remaining_story_points
    #         })
            
    #     # Log the complete burndown data
    #     logger.debug(f">>> === burndown_data: {burndown_data} === <<<")
