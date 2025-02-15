from app_organization.mod_project.models_project import *

from app_organization.mod_app.all_view_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.forms_backlog import *
from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_collection.models_collection import *

from app_organization.mod_step.models_step import *
from app_jivapms.mod_app.all_view_imports import *

from app_common.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'backlog'
module_path = f'mod_backlog'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
# viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
# first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}

def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list_backlogs(request, pro_id, parent_id):
    # take inputs
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    parent = None
    ctypes = None
    if parent_id !=0 and parent_id is not None:
        parent = get_object_or_404(Backlog, pk=parent_id, pro_id=pro_id, 
                                   **viewable_dict)
        ctypes = BacklogType.objects.filter(pk=parent.type_id, pro_id=pro_id ).order_by('position')
        
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    search_query = request.GET.get('search', '')
    deleted_count = 0
    
    # breadcrumbs 
    # Get the current content object if not at root
    current_content = None
    breadcrumbs = []
    if parent_id:
        current_content = get_object_or_404(Backlog, pk=parent_id, pro_id=pro_id)
        breadcrumbs = list(current_content.get_ancestors(include_self=True))
        
    if search_query:
        tobjects = Backlog.objects.filter(name__icontains=search_query, 
                                            parent_id=parent_id,
                                            pro_id=pro_id,
                                            active=True,deleted=False, **viewable_dict ).order_by('position')
        deleted = Backlog.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = Backlog.objects.filter(active=True, parent_id=parent_id,
                                                pro_id=pro_id,
                                                **viewable_dict).order_by('position')
        deleted = Backlog.objects.filter(active=False,  parent_id=parent_id, 
                                               pro_id=pro_id,
                                               deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        #print(f">>> === show_all: {show_all} === <<<")   
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
            
        if 'selected_item' in request.POST:  
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(Backlog, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Backlog, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Backlog, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Backlog, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id)
            return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id)
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_backlogs',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'ref_parent_id': ref_parent_id,  
        'parent': parent,
        'parent_id': parent_id,  
        'ctypes': ctypes,
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
        'breadcrumbs': breadcrumbs,
        'page_title': f'Backlog List',
    }       
    template_file = f"{app_name}/{module_path}/list__backlogs.html"
    return render(request, template_file, context)



# list the deleted objects
# ============================================================= #
@login_required
def list_deleted_backlogs(request, pro_id, parent_id):
    # take inputs
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    # process inputs
    user = request.user        
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None

    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25    
    search_query = request.GET.get('search', '')
    
    # breadcrumbs 
    # Get the current content object if not at root
    current_content = None
    breadcrumbs = []
    if parent_id:
        current_content = get_object_or_404(Backlog, pk=parent_id)
        breadcrumbs = list(current_content.get_ancestors(include_self=True))
    
    if search_query:
        tobjects = Backlog.objects.filter(name__icontains=search_query, 
                                                pro_id=pro_id,
                                            parent_id=parent_id,
                                            **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = Backlog.objects.filter(parent_id=parent_id, 
                                                pro_id=pro_id,
                                                active=False, deleted=False, **viewable_dict).order_by('position')
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        print(f">>> === show_all: {show_all} === <<<")   
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
        
        if 'selected_item' in request.POST:  
                selected_items = request.POST.getlist('selected_item')  
                for item_id in selected_items:
                    item = int(item_id)  
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(Backlog, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                        print(f">>> === bulk_restore: {object}{object.active}{object.deleted} === <<<")
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Backlog, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                        print(f">>> === bulk_erase: {object}{object.active}{object.deleted} === <<<")
                    else:
                        return redirect('list_deleted_backlogs', pro_id=pro_id, parent_id=ref_parent_id)
                return redirect('list_deleted_backlogs', pro_id=pro_id, parent_id=ref_parent_id)
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_backlogs',
        'ref_parent_id': ref_parent_id,  
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'parent_id': parent_id,  
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'breadcrumbs': breadcrumbs,
        'page_title': f'Backlog List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted__backlogs.html"
    return render(request, template_file, context)



# # Create View
# @login_required
# def create_backlog(request, pro_id, parent_id):
#     user = request.user
#     ref_parent_id = parent_id
#     parent_id = None if parent_id == 0 else parent_id
#     viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
#                                 viewable_flag, first_viewable_flag)
#     # connect with connect id
#     pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
#     stored_selected_id = None
#     form = None
#     if request.method == 'POST':
#         action = request.POST.get('action', None)
#         if action == 'select_id':
#             selected_id = request.POST.get('selected_id')
#             request.session['selected_id'] = selected_id
#             stored_selected_id = selected_id
#             ctype = BacklogType.objects.get(pk=selected_id)
#             print(f">>> === selected_id: {selected_id} === <<<")
#             form = BacklogForm(initial={'type': ctype})
#             context = {
#                 'parent_page': '___PARENTPAGE___',
#                 'page': 'create_backlog',
#                 'pro_id': pro_id,
#                 'pro': pro,
#                 'project': pro,
#                 'org': pro.org,
#                 'org_id': pro.org_id,
#                 'ref_parent_id': ref_parent_id,
#                 'parent_id': parent_id,
#                 'selected_id': selected_id,
#                 'ctype': ctype,
#                 'form': form,
#                 'page_title': f'Create Backlog',
#             }
#             template_file = f"{app_name}/{module_path}/create__backlog.html"
#             return render(request, template_file, context)
        
#         elif action == 'create_content':
#             form = BacklogForm(request.POST)
#             if form.is_valid():
#                 print(f">>> === stored id : {stored_selected_id} === <<<")
#                 selected_id = request.session.get('selected_id')
#                 request.session['selected_id'] = None
#                 form.instance.type_id = selected_id
#                 form.instance.pro_id = pro_id
#                 form.instance.parent_id = parent_id
#                 form.instance.author = user
#                 form.save()
#                 return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id)
#             else:
#                 print(f">>> === form.errors: {form.errors} === <<<")
   
#     else:
#         form = BacklogForm()

#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'create_backlog',
#         'pro_id': pro_id,
#         'pro': pro,
#         'project': pro,
#         'org': pro.org,
#         'org_id': pro.org_id,
#         'ref_parent_id': ref_parent_id,  
#         'parent_id': parent_id,  
#         'module_path': module_path,
#         'form': form,
#         'page_title': f'Create Backlog',
#     }
#     template_file = f"{app_name}/{module_path}/create__backlog.html"
#     return render(request, template_file, context) 



# Create View
@login_required
def create_backlog(request, pro_id, parent_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    stored_selected_id = None
    form = None
    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'select_id':
            selected_id = request.POST.get('selected_id')
            request.session['selected_id'] = selected_id
            stored_selected_id = selected_id
            ctype = BacklogType.objects.get(pk=selected_id)
            print(f">>> === selected_id: {selected_id} === <<<")
            form = BacklogForm(initial={'type': ctype})
            context = {
                'parent_page': '___PARENTPAGE___',
                'page': 'create_backlog',
                'pro_id': pro_id,
                'pro': pro,
                'project': pro,
                'org': pro.org,
                'org_id': pro.org_id,
                'ref_parent_id': ref_parent_id,
                'parent_id': parent_id,
                'selected_id': selected_id,
                'ctype': ctype,
                'form': form,
                'page_title': f'Create Backlog',
            }
            template_file = f"{app_name}/{module_path}/create__backlog.html"
            return render(request, template_file, context)
        
        elif action == 'create_content':
            form = BacklogForm(request.POST)
            if form.is_valid():
                print(f">>> === stored id : {stored_selected_id} === <<<")
                selected_id = request.session.get('selected_id')
                request.session['selected_id'] = None
                form.instance.type_id = selected_id
                form.instance.pro_id = pro_id
                form.instance.parent_id = parent_id
                form.instance.author = user
                form.save()
                return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id)
            else:
                print(f">>> === form.errors: {form.errors} === <<<")
   
    else:
        form = BacklogForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Backlog',
    }
    template_file = f"{app_name}/{module_path}/create__backlog.html"
    return render(request, template_file, context) 


# Edit
@login_required
def edit_backlog(request, pro_id, parent_id,  content_id):
    logger.debug(f">>> === edit_backlog: PARENT_ID: {parent_id}:{pro_id}:{content_id} === <<<")
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(Backlog, pk=content_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = BacklogForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.parent_id = parent_id
            form.instance.pro_id = pro_id
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id)
    else:
        form = BacklogForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Backlog',
    }
    template_file = f"{app_name}/{module_path}/edit__backlog.html"
    return render(request, template_file, context)


@login_required
def delete_backlog(request, pro_id, parent_id, content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(Backlog, pk=content_id, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Backlog',
    }
    template_file = f"{app_name}/{module_path}/delete__backlog.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_backlog(request, pro_id, parent_id, content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(Backlog, pk=content_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id)
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Backlog',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion__backlog.html"
    return render(request, template_file, context)


@login_required
def restore_backlog(request, pro_id, parent_id, content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(Backlog, pk=content_id, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id)


@login_required
def view_backlog(request, pro_id, parent_id,  content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(Backlog, pk=content_id, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'module_path': module_path,
        'project': pro,
        'content_id': content_id,
        'backlog': object,
        'org': pro.org,
        'org_id': pro.org_id,
        'page_title': f'View Backlog',
    }
    template_file = f"{app_name}/{module_path}/view__backlog.html"
    return render(request, template_file, context)

@login_required
def project_backlog_decide(request, pro_id):
    user = request.user
    pro = get_object_or_404(Project, pk=pro_id)
   

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'backlog_decide',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'org_id': pro.org_id,
       
        'module_path': module_path,
        'project': pro,
        'object': pro,

        'page_title': f'Backlog',
    }
    template_file = f"{app_name}/{module_path}/project_backlog.html"
    return render(request, template_file, context)

@login_required
def copy_backlog(request, pro_id , parent_id, content_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    tobject = get_object_or_404(Backlog, id=content_id, 
                                pro_id = pro_id, 
                                **viewable_dict, active=True,
                                author=user)

    # clone the tree db given
    fields_to_copy = ['name', 'description', 'type', 'pro', 'position', 'author']  # Specify fields you want to copy
    cloned_treedb = clone_mptt_tree(Backlog, tobject, fields=fields_to_copy)
    cloned_treedb.pro_id = pro_id
    cloned_treedb.parent_id = parent_id
    cloned_treedb.save()

    return redirect('list_backlogs', pro_id=pro_id, parent_id=ref_parent_id) 


def build_serial_number_tree(node, current_path=[], serial_no=None):
    if serial_no is None:
        serial_no = defaultdict(int)  

    level = len(current_path)
    serial_no[level] += 1

    node_serial = '.'.join(map(str, current_path + [serial_no[level]]))
    result = [(node, node_serial)]   
    child_levels = list(range(level + 1, max(serial_no.keys()) + 1))
    for l in child_levels:
        serial_no[l] = 0

    children = node.get_children().order_by('position')
    for child in children:
        result.extend(build_serial_number_tree(child, current_path + [serial_no[level]], serial_no))

    return result


# Function to fetch a node by ID and generate its subtree with serial numbers
def get_serialized_subtree_from_node(request, node_id):
    user = request.user
    try:
        node = Backlog.objects.get(id=node_id, active=True, author=user)
        return build_serial_number_tree(node)
    except Backlog.DoesNotExist:
        return []
    


@login_required
def view_backlog_tree(request, pro_id, parent_id):
    # take inputs
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # process inputs
    
    workspace = None
    wslist = None
    objects_per_page = 100
    objects_count = 0
    
    parent = get_object_or_404(Backlog, id=parent_id, author=user)
    children = None 
    ancestors = None
    root = parent.get_root()
    root_workspace = None
      
    if not parent.is_leaf_node():
        children = parent.get_active_children()    
    if not children:
        ancestors = parent.get_ancestors()
        
    if children != None:
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]    

    ## Check whether an workspace item exists in treedb
    treedb = Backlog.objects.filter(id=parent_id, 
                                          pro_id=pro_id,
                                          **viewable_dict,
                                          author=user).first()

    if treedb:
        wslist = treedb.get_active_children().order_by('position')
        objects_count = wslist.count()
        #print(f">>> === Getting Tree wslist: {wslist} === <<<")
    show_all = request.GET.get('all', 'false').lower() == 'true'
   
    if show_all:
        # No pagination, show all records
        page_obj = wslist
        serialized_nodes = get_serialized_subtree_from_node(request, pk)
    else:
        paginator = Paginator(wslist, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serialized_nodes = get_serialized_subtree_from_node(request, pk)
    
    
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'view_backlog_tree',
        'user': user,
        'ancestors': ancestors,

        'wslist': wslist,
        'treedb': treedb,
        'root': root,

        'serialized_nodes': serialized_nodes,
    
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'page_title': f'Backlog Tree View',
    }       
    template_file = f"{app_name}/{module_path}/view__backlog_tree.html"
    return render(request, template_file, context)    
    

# def build_serial_number_tree(node, current_path=[], serial_no=None):
#     if serial_no is None:
#         serial_no = defaultdict(int)  

#     level = len(current_path)
#     serial_no[level] += 1

#     node_serial = '.'.join(map(str, current_path + [serial_no[level]]))
#     result = [(node, node_serial)]   
#     child_levels = list(range(level + 1, max(serial_no.keys()) + 1))
#     for l in child_levels:
#         serial_no[l] = 0

#     children = node.get_children().order_by('position')
#     for child in children:
#         result.extend(build_serial_number_tree(child, current_path + [serial_no[level]], serial_no))

#     return result
def build_serial_number_tree(node, current_path=[], serial_no=None):
    if serial_no is None:
        serial_no = defaultdict(int)  

    level = len(current_path)
    serial_no[level] += 1

    # Debug the current node and its parent
    parent_id = node.parent.id if node.parent else 0
    #print(f"Node ID: {node.id}, Name: {node.name}, Parent ID: {parent_id}")

    node_serial = '.'.join(map(str, current_path + [serial_no[level]]))
    result = [(node, node_serial, parent_id)]  # Include parent ID

    child_levels = list(range(level + 1, max(serial_no.keys()) + 1))
    for l in child_levels:
        serial_no[l] = 0

    children = node.get_children().order_by('position')
    for child in children:
        if child.active == True:
            result.extend(build_serial_number_tree(child, current_path + [serial_no[level]], serial_no)) 

    return result



# Function to fetch a node by ID and generate its subtree with serial numbers
def get_serialized_subtree_from_node(request, node_id):
    user = request.user
    try:
        node = Backlog.objects.get(id=node_id, active=True)
        return build_serial_number_tree(node)
    except Backlog.DoesNotExist:
        return []
    
@login_required
def view_tree__backlog(request, pro_id, parent_id):
    # take inputs
    user = request.user
    ref_parent_id = parent_id
    form = None
    form = BacklogForm()
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    # process inputs
    
    workspace = None
    wslist = None
    objects_per_page = 100
    objects_count = 0
    
    parent = get_object_or_404(Backlog, id=parent_id)
    children = None 
    ancestors = None
    root = parent.get_root()
    root_workspace = None
      
    if not parent.is_leaf_node():
        children = parent.get_active_children()    
    if not children:
        ancestors = parent.get_ancestors()
        
    if children != None:
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]    

    ## Check whether an workspace item exists in treedb
    treedb = Backlog.objects.filter(id=parent_id, 
                                          pro_id=pro_id,
                                         
                                          ).first()

    if treedb:
        wslist = treedb.get_active_children().order_by('position')
        objects_count = wslist.count()
        #print(f">>> === Getting Tree wslist: {wslist} === <<<")
    show_all = request.GET.get('all', 'false').lower() == 'true'
   
    if show_all:
        # No pagination, show all records
        page_obj = wslist
        serialized_nodes = get_serialized_subtree_from_node(request, parent_id)
    else:
        paginator = Paginator(wslist, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serialized_nodes = get_serialized_subtree_from_node(request, parent_id)
    
    
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'view_tree__backlog',
        'user': user,
        'ancestors': ancestors,

        'wslist': wslist,
        'treedb': treedb,
        'root': root,
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'object': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'ref_parent_id': ref_parent_id,
        'parend_id': parent_id,
        'serialized_nodes': serialized_nodes,
        'form': form,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'page_title': f'Backlog Tree View',
    }       
    template_file = f"{app_name}/{module_path}/view_tree__backlog.html"
    return render(request, template_file, context)    
    
# Release and Iteration Processing
@login_required
def ajax_get_iterations(request, release_id):
    
    iterations = OrgIteration.objects.filter(org_release_id=release_id, active=True)
    data = [{'id': iteration.id, 'name': iteration.name} for iteration in iterations]

    return JsonResponse(data, safe=False)


@login_required
def ajax_get_release_iterations(request):
    release_id = request.POST.get('release_id')

    if release_id:
        iterations = OrgIteration.objects.filter(org_release_id=release_id, active=True).values('id', 'name')
        return JsonResponse({"iterations": list(iterations)})

    return JsonResponse({"error": "Invalid release ID"}, status=400)
    iterations = OrgIteration.objects.filter(org_release_id=release_id, active=True)
    data = [{'id': iteration.id, 'name': iteration.name} for iteration in iterations]

    return JsonResponse(data, safe=False)



@login_required
def iterate__backlog(request, pro_id, parent_id):
    # take inputs
    user = request.user
    ref_parent_id = parent_id
    form = None
    form = BacklogForm()
    parent_id = None if parent_id == 0 else parent_id
   
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id)
    # process inputs
    
    workspace = None
    wslist = None
    objects_per_page = 100
    objects_count = 0
    
    parent = get_object_or_404(Backlog, id=parent_id)
    children = None 
    ancestors = None
    root = parent.get_root()
    root_workspace = None
      
    if not parent.is_leaf_node():
        children = parent.get_active_children()    
    if not children:
        ancestors = parent.get_ancestors()
        
    if children != None:
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]    

    ## Check whether an workspace item exists in treedb
    treedb = Backlog.objects.filter(id=parent_id, 
                                          pro_id=pro_id,
                                         
                                          ).first()

    if treedb:
        wslist = treedb.get_active_children().order_by('position')
        objects_count = wslist.count()
        #print(f">>> === Getting Tree wslist: {wslist} === <<<")
    show_all = request.GET.get('all', 'false').lower() == 'true'
   
    if show_all:
        # No pagination, show all records
        page_obj = wslist
        serialized_nodes = get_serialized_subtree_from_node(request, parent_id)
    else:
        paginator = Paginator(wslist, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serialized_nodes = get_serialized_subtree_from_node(request, parent_id)
    
    
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'iterate',
        'user': user,
        'ancestors': ancestors,

        'wslist': wslist,
        'treedb': treedb,
        'root': root,
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'object': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'ref_parent_id': ref_parent_id,
        'parend_id': parent_id,
        'serialized_nodes': serialized_nodes,
        'form': form,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'page_title': f'Iterate Backlog',
    }       
    template_file = f"{app_name}/{module_path}/iterate__backlog.html"
    return render(request, template_file, context)    



@login_required
def story_mapping_backlog(request, pro_id, parent_id):
    # take inputs
    user = request.user
    ref_parent_id = parent_id
    form = None
    form = BacklogForm()
    parent_id = None if parent_id == 0 else parent_id
    
    # Mapped story ids 
    mappings = StoryMapping.objects.filter(active=True)
    print(f">>> === Mappings: {mappings} === <<<")
    mapped_story_ids = mappings.values_list('story_id', flat=True)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id)
    organization = pro.org
    # process inputs
   
            
    ############################ STORY MAPPING ################################
    # getting the release
    release = None
    releases = OrgRelease.objects.filter(org=organization, active=True).prefetch_related('org_release_org_iterations')
    # Fetch all personas to populate the dropdown
    personae = Persona.objects.filter(active=True, organization=organization)
    
    workspace = None
    wslist = None
    objects_per_page = 100
    objects_count = 0
    
    parent = get_object_or_404(Backlog, id=parent_id)
    children = None 
    ancestors = None
    root = parent.get_root()
    root_workspace = None
      
    if not parent.is_leaf_node():
        children = parent.get_active_children()    
    if not children:
        ancestors = parent.get_ancestors()
        
    if children != None:
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]    

    ## Check whether an workspace item exists in treedb
    treedb = Backlog.objects.filter(id=parent_id, 
                                          pro_id=pro_id,
                                         
                                          ).first()

    if treedb:
        wslist = treedb.get_active_children().order_by('position')
        objects_count = wslist.count()
        #print(f">>> === Getting Tree wslist: {wslist} === <<<")
    show_all = request.GET.get('all', 'false').lower() == 'true'
   
    if show_all:
        # No pagination, show all records
        page_obj = wslist
        serialized_nodes = get_serialized_subtree_from_node(request, parent_id)
    else:
        paginator = Paginator(wslist, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serialized_nodes = get_serialized_subtree_from_node(request, parent_id)
    
    
    releases_json = [
        {
            "id": release.id,
            "name": release.name,
            "iterations": [
                {"id": iteration.id, "name": iteration.name}
                for iteration in release.org_release_org_iterations.filter(active=True)
            ]
        }
        for release in releases
    ]
    
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'iterate',
        'user': user,
        'ancestors': ancestors,
        'releases': releases,
        'list_releases':  json.dumps(releases_json),
        'wslist': wslist,
        'treedb': treedb,
        'root': root,
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'object': pro,
        'org': pro.org,
        'org_id': pro.org_id,
        'personae': personae,
        'ref_parent_id': ref_parent_id,
        'mappings': mappings,
        'mapped_story_ids': mapped_story_ids,
        'parent_id': parent_id,
        'serialized_nodes': serialized_nodes,
        'form': form,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'page_title': f'Iterate Backlog',
    }       
    template_file = f"{app_name}/{module_path}/story_mapping_backlog.html"
    return render(request, template_file, context)    



@login_required
def ajax_fetch_persona_activities1(request):
    # Get persona_id from POST data
    persona_id = request.POST.get('persona_id')
    persona = Persona.objects.get(id=persona_id)
    organization = persona.organization
    #Persona.objects.all().delete()
    # Proceed only if persona_id is provided
    if persona_id:
        try:
            # Fetch the persona based on the provided ID
            persona = Persona.objects.get(id=persona_id)
            
            
            # Fetch activities related to the persona and prefetch related steps
            activities = Activity.objects.filter(persona=persona, active=True).prefetch_related('activity_steps')
            
            # Prepare the data to be sent as JSON
            activities_data = [{
                'id': activity.id,
                'name': activity.name,
                'steps': [{'id': step.id, 'name': step.name} for step in activity.activity_steps.filter(active=True)]
            } for activity in activities]
            
            # Return the activities and their steps as JSON
            return JsonResponse({'activities': activities_data}, safe=False)
        
        except Persona.DoesNotExist:
            # Handle the case where the persona is not found
            return JsonResponse({'error': 'Persona not found'}, status=404)
    else:
        # Persona ID was not provided in the POST request
        return JsonResponse({'error': 'No persona selected'}, status=400)


# views.py


def ajax_fetch_persona_activities(request):
    if request.method == 'POST':
        persona_id = request.POST.get('persona_id')
        activities = Activity.objects.filter(persona_id=persona_id, active=True).prefetch_related('activity_steps')
        mappings = StoryMapping.objects.filter(persona_id=persona_id, active=True)

        activities_data = []
        for activity in activities:
            steps = activity.activity_steps.filter(active=True)
            steps_data = [{'id': step.id, 'name': step.name} for step in steps]
            activities_data.append({
                'id': activity.id,
                'name': activity.name,
                'steps': steps_data,
            })

        mappings_data = []
        for mapping in mappings:
            mappings_data.append({
                'story_name': mapping.story_name,
                'story_id': mapping.story_id,
                'release_id': mapping.release_id if mapping.release_id else None,
                'iteration_id': mapping.iteration_id if mapping.iteration_id else None,
                'activity_id': mapping.activity_id if mapping.activity_id else None,
                'step_id': mapping.step_id if mapping.step_id else None,
                'persona_id': mapping.persona_id if mapping.persona_id else None,
            })

        return JsonResponse({
            'activities': activities_data,
            'mappings': mappings_data,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def ajax_recieve_story_mapped_details(request):
    try:
        # Parse JSON data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body.")
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        
        # Extract required parameters
        try:
            project_id = data['project_id']
            story_id = data['story_id']
            release_id = data['release_id']
            iteration_id = data.get('iteration_id', None)
            activity_id = data['activity_id']
            step_id = data['step_id']
            persona_id = data['persona_id']
            
        except KeyError as e:
            missing_key = str(e)
            logger.error(f"Missing required parameter: {missing_key}")
            return JsonResponse({"status": "error", "message": f"Missing required parameter: {missing_key}"}, status=400)
        
        # Handle '-1' as None for iteration_id
        if iteration_id == '-1':
            iteration_id = None
        
        # Log extracted data
        logger.debug(f"Received Data: {data}")
        
        # Transaction block to ensure atomicity
        with transaction.atomic():
            try:
                # Fetch the story details
                project = Project.objects.get(id=project_id)
                persona = Persona.objects.get(id=persona_id)
                story_details = Backlog.objects.get(id=story_id)
                logger.debug(f"Fetched Story Details: {story_details}")
                # Validate release_id
                try:
                    release = OrgRelease.objects.get(id=release_id)  # Validate foreign key
                except OrgRelease.DoesNotExist:
                    logger.error(f"Invalid Release ID: {release_id}")
                    return JsonResponse({"status": "error", "message": f"Release ID {release_id} does not exist"}, status=400)

                # Save or update the story mapping
                mapping, created = StoryMapping.objects.update_or_create(
                    story_id=story_id,
                    backlog_ref=story_details,
                    defaults={
                        'pro_id': project_id,
                        'persona_id': persona_id,
                        'mapped_at': timezone.now(),
                        'active': True,
  
                        'release_id': release_id,
                        'iteration_id': iteration_id,
                        'activity_id': activity_id,
                        'step_id': step_id,
                    }
                )

                # Determine the result message
                message = "Story mapped successfully." if created else "Story mapping updated successfully."
                logger.info(f"Story Mapping: {message}")


                # current update the backlog as type user story
                # 1. find the user story type for the org
                # 2. update the story type to user story
                # backlog_types = BacklogType.objects.filter(active=True)
                # print(f">>> === Backlog Types: {backlog_types} === <<<")
                backlog_type = None
                if BacklogType.objects.filter(pro=project, name='User Story').exists():
                    project_id_str = f"{project.id}_PROJECT_TREE"
                    backlog_type_root = BacklogType.objects.get(pro=project, parent__name=project_id_str)
                    backlog_types = backlog_type_root.get_descendants(include_self=True)
                    backlog_type = None
                    for backlog_type_read in backlog_types:
                        if backlog_type_read.name == 'User Story':
                            backlog_type = backlog_type_read
                            break
                    logger.debug(f">>> === Backlog Type: US {backlog_type} EXISTS for project: {project} {project.id}=== <<<")
                else:
                    backlog_type = BacklogType.objects.create(pro=project, name='User Story', active=True)
                    logger.debug(f">>> === Backlog Type: US {backlog_type} created for project: {project} {project.id}=== <<<")
                
                
                
                story_details.type = backlog_type                
                story_details.project = project
                story_details.persona = persona                
                story_details.release = release 
                story_details.iteration_id = iteration_id
                story_details.save()
                logger.debug(f"Updated Backlog Release ID: {story_details.release_id}")

                # Return success response
                response = {"status": "success", "message": message}
                logger.debug(f"Response: {response}")
                return JsonResponse(response)

            except Backlog.DoesNotExist:
                logger.error(f"Story with ID {story_id} not found in Backlog.")
                return JsonResponse({"status": "error", "message": "Story not found"}, status=404)
            except Exception as e:
                logger.error(f"Error during transaction: {str(e)}")
                logger.error(traceback.format_exc())
                return JsonResponse({"status": "error", "message": "An unexpected error occurred"}, status=500)

    except Exception as e:
        # Catch any other unexpected exceptions
        logger.error(f"Unhandled error: {str(e)}")
        logger.error(traceback.format_exc())
        return JsonResponse({"status": "error", "message": "An unexpected error occurred"}, status=500)

   
@login_required
def ajax_story_back_to_list(request):
    try:
        data = json.loads(request.body)  # Correctly parsing JSON data from the request body
        story_id = data['story_id']
       
        print(f">>> === Back to List: Story ID: {story_id} === <<<")
        # Perform a soft delete by setting `active` to False
        updated_count = StoryMapping.objects.filter(
            Q(story_id=story_id) & Q(active=True)
        ).update(active=False)

        if updated_count > 0:
            message = "Story mapping cleared successfully."
        else:
            message = "No active mapping found for the given story."
        
        # Further processing and validation can go here

        return JsonResponse({"status": "success", "message": "Story Mapped successfully."})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except KeyError:
        return JsonResponse({"status": "error", "message": "Missing required parameters"}, status=400)
    
    
@login_required
def view_flat_backlog(request, pro_id, parent_id):
    user = request.user
    member = get_object_or_404(Member, user=user)
    project = Project.objects.get(id=pro_id)
    
    # BacklogType for FLAT_BACKLOG_TYPES
    for key, value in FLAT_BACKLOG_NAME_ICONS.items():
        backlog_type, created = BacklogType.objects.get_or_create(
            name=value["name"], 
            pro=project, 
            active=True
        )
        print(f">>> === BacklogType: {backlog_type}, Created: {created} === <<<")

    
    # Filter BacklogTypes based on the COMMON_BACKLOG_TYPES dictionary
    flat_backlog_root = Backlog.objects.filter(pro=project, name=FLAT_BACKLOG_ROOT_NAME).first()
    filters = {}
    
    # Extract filter_by parameter
    filter_by = request.GET.get('filter_by', '').strip()  # Default to empty string if not provided

    # Handle "unmapped" case
    if filter_by == 'unmapped':
        filters['parent'] = None
        #print(f">>> === Filters unmapped: {filters} unmapped === <<<")
   
    elif filter_by == 'all_items':
        filters = {}
        #print(f">>> === Filters allitems: {filters} all_items === <<<")
    elif filter_by.startswith('filter_'):
        # Extract the collection ID from the filter_by parameter
        collection_id = filter_by.replace('filter_', '')
        if collection_id.isdigit():  # Ensure it's a valid numeric ID
            filters['parent_id'] = int(collection_id)
            #print(f">>> === Filters Collection: {filters} match === <<<")
   
    
    #
    # This is where the backlog items are selected for display
    # can be filtered based on collections
    #
    backlog_types = BacklogType.objects.filter(
        active=True, 
        name__in=[item["name"] for item in FLAT_BACKLOG_NAME_ICONS.values()]
    ).select_related('type')

    # Collect backlog items for the filtered backlog types
    backlog_deleted = False
    backlog_deleted_count = Backlog.objects.filter(
                            pro_id=pro_id,
                            active=False
                            ).count()
    if backlog_deleted_count > 0:
        backlog_deleted = True
    if filter_by == "deleted":
        backlog_items = Backlog.objects.filter(
            pro_id=pro_id,
            active=False
        ).order_by('position', '-created_at')
    else:
        backlog_items = Backlog.objects.filter(
            pro_id=pro_id,
            type__in=backlog_types, 
            **filters,
            active=True
        ).order_by('position', '-created_at')
    backlog_items_count = backlog_items.count()
    
    # find out the flat backlog for this project
    
    flat_backlog_collection_type = BacklogType.objects.filter(name='Collection').first() 
    if not flat_backlog_collection_type:
        flat_backlog_collection_type = BacklogType.objects.create(
            name='Collection',
            pro=project,
            active=True,
        )
    
    # demo collections for testing
    db_collections = Collection.objects.filter(project=project, active=True)
    backlog_collections = Backlog.objects.filter(pro=project, type=flat_backlog_collection_type, parent=flat_backlog_root)

 
    # Step 1: Create a mapping of `Collection` IDs to their respective objects
    db_collection_map = {dc.id: dc for dc in db_collections}

    # Step 2: Track `Backlog` entries to determine which need to be removed
    backlog_ids_to_keep = set()

    # Step 3: Sync existing `Backlog` items with the corresponding `Collection` items
    for bdc in backlog_collections:
        if bdc.collection == None:
            continue
        collection = db_collection_map.get(bdc.collection.id)

        if collection:
            backlog_ids_to_keep.add(bdc.id)

            if not collection.active:
                # Soft delete case: mark backlog as inactive
                if bdc.active:
                    bdc.active = False
                    bdc.save()
            else:
                # Update name and active status if necessary
                if bdc.name != collection.name:
                    bdc.name = collection.name
                if not bdc.active:
                    bdc.active = True
                bdc.save()
        else:
            # Collection no longer exists; this backlog item should be removed
            bdc.active = False
            bdc.save()
             # Update child items to detach from the deactivated parent
            child_backlogs = Backlog.objects.filter(parent=bdc)
            child_backlogs.update(parent=flat_backlog_root, collection=None)

    # Step 4: Add missing `Collection` items to the `Backlog`
    existing_collection_ids = {bdc.collection.id for bdc in backlog_collections if bdc.collection is not None}

    for collection in db_collections.filter(active=True):  # Only add active collections
        if collection.id not in existing_collection_ids:
            Backlog.objects.create(
                pro=project,
                type=flat_backlog_collection_type,
                name=collection.name,
                collection=collection,
                created_by=user,
                position=0,
                parent=flat_backlog_root,
                author=user,
            )

        
                
    collections = Backlog.objects.filter(pro=project, type=flat_backlog_collection_type, parent=flat_backlog_root, active=True)
    if request.method == 'POST':
        
        
        backlog_summary = request.POST.get('backlog_summary')
        add_action = request.POST.get('add_action')
        action = request.POST.get('read_action', '').strip().lower()
        collection_id = request.POST.get("collection_id")
        selected_items = request.POST.get("selected_items", "").split(",")
        type_of_bi = request.POST.get("type")
        
        if action == 'assign':
            #print(f">>> === Assigning Items: {selected_items} to Collection: {collection_id} === <<<")
            for each_item in selected_items:
                backlog_item = Backlog.objects.get(id=each_item)
                if collection_id == 'Others':
                    backlog_item.parent = flat_backlog_root
                elif collection_id == "deleted":
                    backlog_item.active = False
                else:
                    backlog_item.parent = Backlog.objects.get(id=collection_id)
                
                    
                backlog_item.save() 
            messages.success(request, f"Items {selected_items} assigned to collection {collection_id} successfully!")
        elif action == "unassign":
            #print(f">>> === UnAssigning Items: {selected_items} from Collection: {collection_id} === <<<")
            for each_item in selected_items:
                backlog_item = Backlog.objects.get(id=each_item)
                backlog_item.parent = flat_backlog_root
                if collection_id == "deleted":
                    backlog_item.active = True
                backlog_item.save()
            messages.success(request, f"Items {selected_items} unassigned from collection {collection_id} successfully!")
        else:
            messages.error(request, "Invalid action.")
            
        
        if add_action == 'add':
            create_backlog_type = BacklogType.objects.filter(name='User Story').first()
            if type_of_bi:
                other_backlog_type = BacklogType.objects.filter(name=type_of_bi).first() 
                if other_backlog_type == None:
                    create_backlog_type = BacklogType.objects.filter(name='User Story').first()
                else:
                    create_backlog_type = other_backlog_type
            #print(f">>> === Backlog Summary: {backlog_summary} === <<<")
            if 'add_to_top' in request.POST:
                #print(f">>> === Backlog Item ADD TO TOP : {create_backlog_type} === <<<")
                backlog_item = Backlog.objects.create(
                    pro=project,
                    type=create_backlog_type,
                    name=backlog_summary,
                    created_by=user,
                    position=0, 
                    parent=flat_backlog_root,
                    author=user,
                )
                #print(f">>> === Backlog Item ADD TO TOP : {backlog_item} {backlog_item.type} {backlog_item.position} {backlog_item.pro} === <<<")
                
            if 'add_to_bottom' in request.POST:
                max_position = Backlog.objects.filter(pro=project).aggregate(models.Max('position'))['position__max']
                new_position = max_position + 1 if max_position is not None else 0

                backlog_item = Backlog.objects.create(
                    pro=project,
                    type=create_backlog_type,
                    name=backlog_summary,
                    created_by=user,
                    position=new_position,
                    parent=flat_backlog_root,
                    author=user,
                )
                #print(f">>> === Backlog Item ADD TO BOTTOM: {backlog_item} === <<<")



    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'iterate',
        'user': user,
        'member': member,
        'pro': project,
        'project': project,
        'pro_id': pro_id,
        'org': project.org,
        'org_id': project.org_id,
        'backlog_deleted': backlog_deleted,
        'backlog_deleted_count': backlog_deleted_count,
        'backlog_items': backlog_items,
        'backlog_types': backlog_types,
        'collections': collections,
        'COMMON_BACKLOG_TYPES': COMMON_BACKLOG_TYPES,
        'ICON_MAPPING': ICON_MAPPING,
        'backlog_items_count': backlog_items_count,
        'page_title': f'View Flat Backlog',
        "STATUS_CHOICES": STATUS_CHOICES,
        "SIZE_CHOICES": SIZE_CHOICES,
        "FLAT_BACKLOG_NAME_ICONS": FLAT_BACKLOG_NAME_ICONS,
    }       
    template_file = f"{app_name}/{module_path}/view_flat_backlog.html"
    return render(request, template_file, context)

