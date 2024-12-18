
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_org_board.models_org_board import *
from app_organization.mod_org_board.forms_org_board import *

from app_organization.mod_organization.models_organization import *
from app_organization.mod_project.models_project import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog_super_type.models_backlog_super_type import *
from app_organization.mod_backlog_type.models_backlog_type import *

from app_common.mod_common.models_common import *

from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'org_boards'
module_path = f'mod_org_board'

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
def list_org_boards(request, org_id):
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
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgBoard.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgBoard.objects.filter(active=True, org_id=org_id).order_by('position')
        deleted = OrgBoard.objects.filter(active=False, deleted=False,
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
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_org_boards', org_id=org_id)
            return redirect('list_org_boards', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_org_boards',
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
        'page_title': f'Org_board List',
    }       
    template_file = f"{app_name}/{module_path}/list_org_boards.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_org_boards(request, org_id):
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
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgBoard.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgBoard.objects.filter(active=False, deleted=False, org_id=org_id,
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
                        object = get_object_or_404(OrgBoard, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OrgBoard, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_org_boards', org_id=org_id)
                redirect('list_org_boards', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_org_boards',
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
        'page_title': f'Org_board List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_org_boards.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_org_board(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = OrgBoardForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_boards', org_id=org_id)
    else:
        form = OrgBoardForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Board',
    }
    template_file = f"{app_name}/{module_path}/create_org_board.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OrgBoardForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_boards', org_id=org_id)
    else:
        form = OrgBoardForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Org Board',
    }
    template_file = f"{app_name}/{module_path}/edit_org_board.html"
    return render(request, template_file, context)



@login_required
def delete_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_org_boards', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Org Board',
    }
    template_file = f"{app_name}/{module_path}/delete_org_board.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_org_boards', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Org Board',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_org_board.html"
    return render(request, template_file, context)


@login_required
def restore_org_board(request,  org_id, org_board_id):
    user = request.user
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_org_boards', org_id=org_id)
   


@login_required
def view_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Org Board',
    }
    template_file = f"{app_name}/{module_path}/view_org_board.html"
    return render(request, template_file, context)




@login_required
def view_project_board(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog collections
    flat_backlog_root = Backlog.objects.filter(pro=project, name=FLAT_BACKLOG_ROOT_NAME).first()
    flat_backlog_collection_type = BacklogType.objects.filter(name='Collection').first() 
    backlog_collections = Backlog.objects.filter(pro=project, type=flat_backlog_collection_type, parent=flat_backlog_root, active=True)
    # send the backlog details of the project
    backlog_types = BacklogType.objects.filter(
        active=True, 
        name__in=FLAT_BACKLOG_TYPES.values(), 
    ).select_related('type')
    filters = {}
    # Get or create the default project board
    DEFAULT_BOARD_NAME = 'Default Board'
    project_board, created = ProjectBoard.objects.get_or_create(
        project=project,
        name=DEFAULT_BOARD_NAME,
        defaults={'author': user}
    )
    
    board_name = ProjectBoard.objects.get(project=project, active=True, name=DEFAULT_BOARD_NAME)

    # Ensure the default columns exist or create them
    DEFAULT_BOARD_COLUMNS = ['ToDo', 'In Progress', 'Blocked', 'Done']
    #ProjectBoardState.objects.all().delete()
    backlog_state = None  # To store the "Backlog" state reference
    for position, column_name in enumerate(DEFAULT_BOARD_COLUMNS):
        state, _ = ProjectBoardState.objects.get_or_create(
            board=project_board,
            name=column_name,
            defaults={'author': user, 'wip_limit': 0}
        )
        if column_name == 'Backlog':
            backlog_state = state

    actual_project_backlog_items = Backlog.objects.filter(
        pro_id=project.id,
        type__in=backlog_types,
        active=True
    ).exclude(
        id__in=ProjectBoardCard.objects.filter(
            board=project_board,
            state__isnull=False  # Exclude items where state.id is NOT NULL (moved to other states)
        ).values_list('backlog_id', flat=True)
    ).order_by('position', '-created_at')    
   
    # Get the project board states
    project_board_states = ProjectBoardState.objects.filter(board=project_board)
    
    # Fetch the project backlog items state
    state_items = {state.name: [] for state in project_board.board_states.filter(active=True)}
   
    # Get the card / backlog item from the ProjectBoardStateTransition
    for state in project_board_states:
        state_items[state.name] = ProjectBoardCard.objects.filter(
            board=project_board,
            state=state,
            active=True,
            backlog__active=True  # Exclude cards linked to soft-deleted Backlog items
        ).select_related('backlog').order_by('position', '-created_at')

    context = {
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'pro_id': project.id,
        'project_board': project_board,
        'project_board_states': project_board_states,
        'backlog_items': actual_project_backlog_items,
        'todo_items': state_items.get('ToDo', []),
        'in_progress_items': state_items.get('In Progress', []),
        'blocked_items': state_items.get('Blocked', []),
        'done_items': state_items.get('Done', []),
        'page_title': f'Project Board: {project.name}',
        
        #'chart_data': chart_data,
    }

    template_file = f"{app_name}/{module_path}/project/view_project_board.html"
    return render(request, template_file, context)

from app_organization.mod_backlog.views_project_tree import create_or_update_tree_from_config, get_tree_name_id
@login_required
def view_project_tree_board(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog types
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_type, created = BacklogType.objects.get_or_create(pro=project, name=pbst_name)
    config = PROJECT_WBS_TREE_CONFIG
    backlog_type_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", parent=project_backlog_type, project=project)
    bt_tree_name_and_id = get_tree_name_id(backlog_type_node)
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id)
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
  
    filters = {}
    # Get or create the default project board
    DEFAULT_BOARD_NAME = 'Default Board'
    project_board, created = ProjectBoard.objects.get_or_create(
        project=project,
        name=DEFAULT_BOARD_NAME,
        defaults={'author': user}
    )
    
    board_name = ProjectBoard.objects.get(project=project, active=True, name=DEFAULT_BOARD_NAME)

    # Ensure the default columns exist or create them
    DEFAULT_BOARD_COLUMNS = ['ToDo', 'In Progress', 'Blocked', 'Done']
    #ProjectBoardState.objects.all().delete()
    backlog_state = None  # To store the "Backlog" state reference
    for position, column_name in enumerate(DEFAULT_BOARD_COLUMNS):
        state, _ = ProjectBoardState.objects.get_or_create(
            board=project_board,
            name=column_name,
            defaults={'author': user, 'wip_limit': 0}
        )
        if column_name == 'Backlog':
            backlog_state = state
    
    actual_project_backlog_items = Backlog.objects.filter(
        pro_id=project.id,
        type__in=backlog_types,
        active=True
    ).exclude(
        id__in=ProjectBoardCard.objects.filter(
            board=project_board,
            state__isnull=False  # Exclude items where state.id is NOT NULL (moved to other states)
        ).values_list('backlog_id', flat=True)
    ).order_by('position', '-created_at')    
   
    # Get the project board states
    project_board_states = ProjectBoardState.objects.filter(board=project_board)
    
    # Fetch the project backlog items state
    state_items = {state.name: [] for state in project_board.board_states.filter(active=True)}
   
    # Get the card / backlog item from the ProjectBoardStateTransition
    for state in project_board_states:
        state_items[state.name] = ProjectBoardCard.objects.filter(
            board=project_board,
            state=state,
            active=True,
            backlog__active=True  # Exclude cards linked to soft-deleted Backlog items
        ).select_related('backlog').order_by('position', '-created_at')

    context = {
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'pro_id': project.id,
        'project_board': project_board,
        'project_board_states': project_board_states,
        'backlog_items': actual_project_backlog_items,
        'todo_items': state_items.get('ToDo', []),
        'in_progress_items': state_items.get('In Progress', []),
        'blocked_items': state_items.get('Blocked', []),
        'done_items': state_items.get('Done', []),
        'page_title': f'Project Board: {project.name}',
        
        #'chart_data': chart_data,
    }

    template_file = f"{app_name}/{module_path}/project/view_project_tree_board.html"
    return render(request, template_file, context)


def update_project_board_state_transition(card, from_state_id, to_state_id):
    if to_state_id == 0:
        # Move to backlog
        to_state_id = None
    if from_state_id == 0:
        # Move from backlog
        from_state_id = None
     # Log the transition
    created_st_entry = ProjectBoardStateTransition.objects.create(
        card=card.backlog,
        from_state_id=from_state_id,
        to_state_id=to_state_id,
        transition_time=now(),
    )
    print(f">>> === Created State Transition: {created_st_entry} === <<<")
    return created_st_entry
                


def column_to_column_update(positions, board_id, card_id, from_column, from_state_id, dest_column, to_state_id):    
    pbc = ProjectBoardCard.objects.get(id=card_id)    
    for pos in positions:
        card_id = pos.get('card_id')
        position = pos.get('position')      
        ProjectBoardCard.objects.filter(id=card_id).update(position=position, state_id=to_state_id)        
    update_project_board_state_transition(pbc, from_state_id, to_state_id)
    return JsonResponse({"success": True})


def column_to_backlog_update(positions, board_id, this_card_id, from_column, from_state_id, dest_column, to_state_id):  
    try:
        # Update the card to have no state (move to backlog)
        card = ProjectBoardCard.objects.get(id=this_card_id)
        card.state = None
        card.position = 0  # Reset position in column
        card.save()
        # Update positions in the Backlog
        for pos in positions:
            backlog_card_id = pos.get('card_id')
            position = pos.get('position')
            if backlog_card_id == card.backlog_id:
                # Update position of the moved backlog item
                Backlog.objects.filter(id=backlog_card_id).update(position=position)
            else:
                # Update positions of other backlog items
                Backlog.objects.filter(id=backlog_card_id).update(position=position)

        update_project_board_state_transition(card, from_state_id, to_state_id)
        return JsonResponse({"success": True})

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)})


def backlog_to_column_update(positions, board_id, this_card_id, from_column, from_state_id, dest_column, to_state_id): 
    try:
        # Fetch or create the ProjectBoardCard for the backlog item
        card, created = ProjectBoardCard.objects.get_or_create(
            backlog_id=this_card_id,
            defaults={"board_id": board_id, "state_id": to_state_id, "position": 0}
        )
        if not created:
            card.state_id = to_state_id  # Move to column
            card.save()
        # Update positions for all cards in the destination column
        for pos in positions:
            card_id = pos.get('card_id')
            position = pos.get('position')            
            if card_id == this_card_id:
                # Update the moved card
                ProjectBoardCard.objects.filter(backlog_id=this_card_id).update(position=position, state_id=to_state_id)
            else:
                # Update other cards in the column
                ProjectBoardCard.objects.filter(id=card_id).update(position=position)       
        update_project_board_state_transition(card, from_state_id, to_state_id)
        return JsonResponse({"success": True})

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)})

def within_column_update(positions, board_id, card_id, dest_column, to_state_id):   
    pbc = ProjectBoardCard.objects.get(id=card_id)    
    for pos in positions:
        card_id = pos.get('card_id')
        position = pos.get('position')     
        ProjectBoardCard.objects.filter(id=card_id).update(position=position)       
    return JsonResponse({"success": True})

def within_backlog_update(positions, board_id, card_id):  
    bi = Backlog.objects.get(id=card_id)    
    for pos in positions:
        card_id = pos.get('card_id')
        position = pos.get('position')       
        Backlog.objects.filter(id=card_id).update(position=position)        
    return JsonResponse({"success": True})

@login_required
def ajax_update_project_board_card_state(request):
    if request.method == "POST":
        data = json.loads(request.body)
        card_id = data.get('card_id')
        board_id = data.get('board_id')
        from_state_id = data.get('from_state_id')
        to_state_id = data.get('to_state_id')

        # position 
        positions = data.get('positions')
        from_column = data.get('from_column')
        dest_column = data.get('dest_column')
        project_id = data.get('project_id')
        board_id = data.get('board_id')
      
        
        if from_state_id == 0 and from_state_id == to_state_id and to_state_id == 0:
            #print(f">>> === Backlog: Within column movement === <<<")
            within_backlog_update(positions, board_id, card_id)
        elif from_state_id !=0 and to_state_id != 0 and from_state_id == to_state_id:
            #print(f">>> === {dest_column}: Within column movement  === <<<")
            within_column_update(positions, board_id, card_id, dest_column, to_state_id)
        elif from_state_id !=0 and to_state_id != 0 and from_state_id != to_state_id:
            #print(f">>> === {from_column} to {dest_column}: Between column movement  === <<<")
            column_to_column_update(positions, board_id, card_id, from_column, from_state_id, dest_column, to_state_id)
        elif from_state_id == 0 and to_state_id != 0:
            #print(f">>> ===  {from_column} to {dest_column}: Between column movement (from Backlog) === <<<")
            backlog_to_column_update(positions, board_id, card_id, from_column, from_state_id, dest_column, to_state_id)
        elif to_state_id == 0 and from_state_id != 0:
            #print(f">>> ===   {from_column} to {dest_column}: Betwee Column Movement (to Backlog)   === <<<")
            column_to_backlog_update(positions, board_id, card_id, from_column, from_state_id, dest_column, to_state_id)

        return JsonResponse({"success": True})


@login_required
def ajax_update_project_board_card_state_REF(request):
    ################################# REF #################################
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_id = data.get('card_id')
            board_id = data.get('board_id')
            from_state_id = data.get('from_state_id')
            to_state_id = data.get('to_state_id')
                      
            # position 
            positions = data.get('dest_positions')
            dest_column = data.get('save_dest_column')
            got_project_id = data.get('send_project_id')
            got_board_id = data.get('send_board_id')
            print(f">>> === GENERAL CHECK dest_column: {dest_column}: position:{positions} === <<<")
            all_states = ProjectBoardState.objects.filter(board_id=board_id).values_list('id', flat=True)
            print(f"Available states for board {board_id}: {list(all_states)}")
            print(f"Incoming dest_column: {dest_column}")
            if dest_column and dest_column != 'Backlog':
                dest_state_qs = ProjectBoardState.objects.filter(name=dest_column, board_id=board_id)
                if dest_state_qs.exists() and dest_state_qs.count() == 1:
                    dest_state = dest_state_qs.first()
                    print(f"Destination State: ID {dest_state.id}, Name: {dest_state.name}")
                    try:
                        with transaction.atomic():
                            for position in positions:
                                card_id = position['card_id']
                                position_value = position['position']

                                card = ProjectBoardCard.objects.get(id=card_id, board_id=board_id)
                                card.state_id = dest_state.id
                                card.position = position_value
                                card.save()

                                print(f"Updated Card ID {card_id} to State {dest_state.id} at Position {position_value}")
                    except Exception as e:
                        print(f"Error during update: {e}")
                        return JsonResponse({"error": "Failed to update cards"}, status=500)
                else:
                    print("Error: Multiple or no states found for the given name and board.")
                    return JsonResponse({"error": "State is ambiguous or not found"}, status=400)

                    
                   
            
            if from_state_id == 0:
                from_state_id = None

                # Validate required fields
                if not (card_id and to_state_id and board_id):
                    return JsonResponse({"error": "Missing required fields"}, status=400)

                try:
                    # Check if the card already exists or create it
                    if to_state_id != 0:
                        card, created = ProjectBoardCard.objects.get_or_create(
                            backlog_id=card_id,  # Use card_id as backlog_id
                            board_id=board_id,
                            defaults={
                                'state_id': to_state_id,
                            }
                        )

                    if created:
                        print(f"Created new ProjectBoardCard: {card}")
                    else:
                        print(f"Found existing ProjectBoardCard: {card}")
                except Exception as e:
                    print(f"Error creating or retrieving ProjectBoardCard: {e}")
                    return JsonResponse({"error": str(e)}, status=500)
                
                # pbc_count = ProjectBoardCard.objects.all().count()
                # print(f">>> === pbc_count: {pbc_count}: {card} === <<<")

                if not created and to_state_id != 0:
                    # If the card already exists, update the state
                    
                    card.state_id = to_state_id
                    card.save()

                return JsonResponse({"success": True, "created": created})                
            else:
                # Fetch the card and states
                card = ProjectBoardCard.objects.get(id=card_id)
                from_state = ProjectBoardState.objects.get(id=from_state_id)
                to_state = None
                if to_state_id == 0:
                    to_state = None
                    print(f">>> === to_state_id: {to_state_id} === <<<")
                else:
                    to_state = ProjectBoardState.objects.get(id=to_state_id)
                # Validate that the card belongs to the current state
                if card.state != from_state:
                    print(f"Card state mismatch: {card.state} != {from_state}")
                    #return JsonResponse({"error": "Card state mismatch"}, status=400)
                
                # Update the card's state
                
                card.state = to_state
                card.save()
                
                # Log the transition
                created_st_entry = ProjectBoardStateTransition.objects.create(
                    card=card.backlog,
                    from_state=from_state,
                    to_state=to_state,
                    transition_time=now(),
                )
                
                # update the status of the backlog item in text for display purposes
                to_state_name = 'Backlog' if to_state_id == 0 else to_state.name
              
                card.backlog.status = to_state_name
                card.backlog.save()
                
             

                return JsonResponse({
                    "message": "Card state updated successfully",
                    "card_id": card.id,
                    "from_state": from_state.name,
                    "to_state": to_state_name,
                })

        except ProjectBoardCard.DoesNotExist:
            return JsonResponse({"error": "Card does not exist"}, status=404)
        except ProjectBoardState.DoesNotExist:
            return JsonResponse({"error": "State does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



def get_cumulative_flow_data(board_id):
    # Fetch all transitions for the board
    # Get the project board instance
    project_board = ProjectBoard.objects.get(id=board_id)

    # Fetch transitions for cards on the board
    transitions = ProjectBoardStateTransition.objects.filter(
        card__board_cards__board=project_board  # Access ProjectBoardCard through Backlog and filter by board
    ).values(
        'card__id',  # Backlog ID
        'from_state__name', 
        'to_state__name', 
        'transition_time'
    )

    # Fetch the min and max dates for transitions
    min_date = transitions.aggregate(Min('transition_time'))['transition_time__min'].date()
    max_date = transitions.aggregate(Max('transition_time'))['transition_time__max'].date()

    # Prepare a mapping of states to daily counts
    states = ProjectBoardState.objects.filter(board=project_board).values_list('name', flat=True)
    state_data = {state: [0] * ((max_date - min_date).days + 1) for state in states}

    # Create a mapping of dates for the range
    date_index = {min_date + timedelta(days=i): i for i in range((max_date - min_date).days + 1)}

    # Process transitions to populate state data
    for transition in transitions:
        card_id = transition['card__id']
        from_state = transition['from_state__name']
        to_state = transition['to_state__name']
        transition_time = transition['transition_time'].date()

        # Increment the state on the respective day
        if to_state in state_data:
            state_data[to_state][date_index[transition_time]] += 1

    # Cumulatively sum the counts for each state
    for state, counts in state_data.items():
        for i in range(1, len(counts)):
            counts[i] += counts[i - 1]

    # Prepare data for Chart.js
    chart_data = {
        "labels": [str(min_date + timedelta(days=i)) for i in range((max_date - min_date).days + 1)],
        "datasets": [
            {
                "label": state,
                "data": counts,
                "fill": "origin"
            } for state, counts in state_data.items()
        ]
    }
    print(f">>> === chart_data: {chart_data} === <<<")
    return chart_data

@login_required
def ajax_update_project_board_card_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_order = data.get("card_order", [])

            # Update positions in the database
            for item in card_order:
                card_id = item.get("card_id")
                position = item.get("position")
                if card_id is not None and position is not None:
                    ProjectBoardCard.objects.filter(id=card_id).update(position=position)

            return JsonResponse({"success": True, "message": "Card positions updated successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)