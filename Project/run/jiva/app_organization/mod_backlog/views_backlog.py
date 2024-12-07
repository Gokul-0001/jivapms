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
    print(f"Node ID: {node.id}, Name: {node.name}, Parent ID: {parent_id}")

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
    
    iterations = Iteration.objects.filter(rel_id=release_id, active=True)
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
    
    
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'iterate',
        'user': user,
        'ancestors': ancestors,
        'releases': releases,
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
def ajax_fetch_persona_activities(request):
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




@login_required
def ajax_recieve_story_mapped_details(request):
    try:
        data = json.loads(request.body)  # Correctly parsing JSON data from the request body
        project_id = data['project_id']
        story_id = data['story_id']
        release_id = data['release_id']
        iteration_id = data['iteration_id']
        activity_id = data['activity_id']
        step_id = data['step_id']
        persona_id = data['persona_id']
        
        story_details = Backlog.objects.get(id=story_id)
        
        print(f">>> === Project ID: {project_id} === <<<")
        print(f">>> === Story ID: {story_id} === <<<")
        print(f">>> === Release ID: {release_id} === <<<")
        print(f">>> === Iteration ID: {iteration_id} === <<<")
        print(f">>> === Activity ID: {activity_id} === <<<")
        print(f">>> === Step ID: {step_id} === <<<")
        print(f">>> === Persona ID: {persona_id} === <<<")
        
        # Check for existing mapping
        existing_mapping = StoryMapping.objects.filter(
            story_id=story_id,
            release_id=release_id,
            iteration_id=iteration_id,
            activity_id=activity_id,
            step_id=step_id,
            persona_id=persona_id,
        ).first()

        if existing_mapping:
            return JsonResponse({"status": "error", "message": "Story is already mapped in this iteration and step."})

        
        # Save or update the story mapping
        mapping, created = StoryMapping.objects.update_or_create(
            pro_id = project_id,
            story_name = story_details.name,
            story_id=story_id,
            release_id=release_id,
            iteration_id=iteration_id,
            activity_id=activity_id,
            step_id=step_id,
            persona_id=persona_id,
            defaults={'mapped_at': timezone.now()}
        )
        
        if created:
            message = "Story mapped successfully."
        else:
            message = "Story mapping updated successfully."

        return JsonResponse({"status": "success", "message": message})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except KeyError:
        return JsonResponse({"status": "error", "message": "Missing required parameters"}, status=400)
    
   
@login_required
def ajax_story_back_to_list(request):
    try:
        data = json.loads(request.body)  # Correctly parsing JSON data from the request body
        story_id = data['story_id']
       
        print(f">>> === Back to List: Story ID: {story_id} === <<<")
       
        
        # Further processing and validation can go here

        return JsonResponse({"status": "success", "message": "Story Mapped successfully."})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except KeyError:
        return JsonResponse({"status": "error", "message": "Missing required parameters"}, status=400)
    