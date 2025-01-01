from app_common.mod_common.models_common import *
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_backlog.models_backlog import *

from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_org_iteration.models_org_iteration import *
from app_organization.mod_persona.models_persona import *
from app_organization.mod_backlog_type.models_backlog_type import *
from app_organization.mod_collection.models_collection import *
from app_common.mod_app.all_view_imports import *


#
#  The idea is the backlog can be flat and have one child element / sub-tasks
#  When needed the backlog can be self-contained with tree structure of own scheme or standard schema
#
# Core Hierarchical System Database
class Backlog(MPTTModel, BaseModelImpl):
  
    persona = models.ForeignKey('app_organization.Persona', on_delete=models.CASCADE,
                                related_name="persona_backlogs", null=True, blank=True)
    
    pro = models.ForeignKey("app_organization.Project", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='backlogs')
    #parent = TreeForeignKey('self', null=True, blank=True, related_name='Project', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
   
    type = TreeForeignKey("app_organization.BacklogType", null=True, blank=True, 
                          related_name='backlog_types', 
                          on_delete=models.CASCADE)
    
    release = models.ForeignKey('app_organization.OrgRelease', on_delete=models.CASCADE, 
                            related_name="backlog_releases", null=True, blank=True)
    
    iteration = models.ForeignKey('app_organization.OrgIteration', on_delete=models.CASCADE, 
                            related_name="backlog_iteration", null=True, blank=True)
     
     
    # refactor 15-22-2024
    flat_backlog_type = models.CharField(max_length=100, choices=FLAT_BACKLOG_TYPES.items(), default='USER STORY')
    size = models.CharField(max_length=100, choices=SIZE_CHOICES, default='0')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Backlog')
    collection = models.ForeignKey('app_organization.Collection', on_delete=models.CASCADE,
                                      related_name="backlog_collections", null=True, blank=True)
    connected_to_hierarchy = models.BooleanField(default=False)
    connected_to_hierarchy_id = TreeForeignKey('self', null=True, blank=True, related_name='Tree', on_delete=models.CASCADE)
    
   
    
    # roadmap
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)    
    progress = models.FloatField(
            default=0.0,
            validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
        )
    # end roadmap   
    
    
    # for now label is a char field
    tag =  models.CharField(max_length=256,null=True, blank=True, default='')
          
   
    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fb_created_by')
    pulled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fb_pulled_by')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name='author_backlogs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='user_backlogs')
   
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Normal')

   
    class MPTTMeta:
        order_insertion_by = ['position', 'created_at']
        
    class Meta:
        ordering = ['position', '-created_at']


    def __str__(self):
        if self.name:
            return self.name
        else:
            return '' + str(self.pk)

    

    def get_cached_completion_stats(self):
        cache_key = f"backlog_completion_{self.pk}"
        stats = cache.get(cache_key)
        if stats is None:
            total_count = self.get_descendants().filter(active=True).count()
            completed_count = self.get_descendants().filter(done=True, active=True).count()
            percent_complete = round((completed_count / total_count) * 100, 2) if total_count > 0 else 0.0
            stats = {'total_count': total_count, 'completed_count': completed_count, 'percent_complete': percent_complete}
            cache.set(cache_key, stats, timeout=300)  # Cache for 5 minutes
        return stats
    
    def get_completion_stats(self):
        total_count = self.get_descendants().filter(done=True, active=True).count() + self.get_descendants().filter(done=False, active=True).count()
        completed_count = self.get_descendants().filter(done=True, active=True).count()
        percent_complete = round((completed_count / total_count) * 100, 2) if total_count > 0 else 0.0
        #print(f"====> {completed_count}/{total_count} ===> {percent_complete}")
        return {
            'total_count': total_count,
            'completed_count': completed_count,
            'percent_complete': percent_complete,
        }
    
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)

    #
    # DEF BLOCK UNBLOCK
    #
    def block(self):
        self.blocked = "blocked"
        self.block_count += 1

    def unblock(self):
        self.blocked = "unblocked"

    ## display 
    def children(self):
        return Backlog.objects.filter(parent=self.pk, active=True)
    
    def serializable_object(self):
        obj = {'name': self.name, 'contents': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj
    
    def get_active_children(self):
        return self.get_children().filter(active=True)
    
    ALLOWED_TRANSITIONS = {
        'Backlog': ['To Do'],
        'To Do': ['In Progress', 'Blocked'],
        'In Progress': ['Done', 'Blocked'],
        'Blocked': ['In Progress', 'Unblocked'],
        'Unblocked': ['In Progress'],
        'Done': ['Backlog', 'Archived', 'Deleted', 'Blocked', 'To Do'],
        # etc.
    }
    def can_transition_to(self, new_status):
        return new_status in self.ALLOWED_TRANSITIONS[self.status]
    
    def update_estimates(self):
        self.estimate = self.sub_tasks.aggregate(total=models.Sum('estimate'))['total'] or 0
        self.save()


    def save(self, *args, **kwargs):
        # Check if the parent backlog item exists
        if self.parent:
            # Validate that the parent is of a flat backlog type
            #print(f"=== >>> {self.parent.flat_backlog_type} ===> {self.flat_backlog_type} === <<<")
            if self.parent.flat_backlog_type not in FLAT_BACKLOG_TYPES:
                raise ValidationError("Subtasks can only be added to flat backlog types.")

            # # Ensure that the parent is not part of a hierarchy
            # print(f"=== >>> {self.parent.get_children()} === <<<")
            # if self.parent.get_children().exists():
            #     raise ValidationError("Cannot add subtasks to a hierarchical backlog item.")
        # Check if the status is being set to "Done"
        if self.flat_backlog_type in FLAT_BACKLOG_TYPES and self.status == "Done":
            # Ensure all subtasks are also marked as "Done"
            incomplete_subtasks = self.sub_tasks.filter(~models.Q(status="Done")).exists()
            if incomplete_subtasks:
                raise ValidationError("Cannot mark the backlog item as 'Done' while subtasks are incomplete.")
        
        # Proceed with saving
        super().save(*args, **kwargs)



# 07122024
# StoryMappingModel

class StoryMapping(BaseModelTrackDateImpl):
    pro = models.ForeignKey("app_organization.Project", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='project_story_mappings')
    backlog_ref = models.ForeignKey(Backlog, on_delete=models.CASCADE, related_name='backlog_ref', null=True, blank=True)
    story_name = models.CharField(max_length=256, null=True, blank=True)
    story_id = models.PositiveIntegerField()  # ID of the story being mapped
    release_id = models.PositiveIntegerField()  # ID of the release
    iteration_id = models.PositiveIntegerField(null=True, blank=True)  # ID of the iteration
    activity_id = models.PositiveIntegerField()  # ID of the activity
    step_id = models.PositiveIntegerField()  # ID of the step
    persona_id = models.PositiveIntegerField()  # ID of the persona
    mapped_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the mapping

    class Meta:
        unique_together = ( 'story_id',)
        verbose_name = 'Story Mapping'
        verbose_name_plural = 'Story Mappings'

    def __str__(self):
        return f"Story {self.story_id} mapped to Release {self.release_id}, Activity {self.activity_id}, Step {self.step_id}, Persona {self.persona_id}"


# 14122024
# adding the flat backlog approach where, user story and similar level types will have sub-tasks

class SubTasks(BaseModelTrackDateImpl):
    parent = models.ForeignKey(Backlog, on_delete=models.CASCADE, related_name='sub_tasks')
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='To Do')
    estimate = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by')
    pulled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pulled_by')
    

    def __str__(self):
        return self.name
    
class ReadyDoneFlags(BaseModelTrackDateImpl):
    backlog_item = models.OneToOneField('app_organization.Backlog', on_delete=models.CASCADE)
    
    # Readiness Flags
    business_ready = models.BooleanField(default=False)
    tech_ready = models.BooleanField(default=False)
    qa_ready = models.BooleanField(default=False)
    ops_ready = models.BooleanField(default=False)

    # Done Flags
    business_done = models.BooleanField(default=False)
    tech_done = models.BooleanField(default=False)
    qa_done = models.BooleanField(default=False)
    ops_done = models.BooleanField(default=False)

    # Summary Flags
    all_ready = models.BooleanField(default=False)
    all_done = models.BooleanField(default=False)

    # Track Changes
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.TextField(blank=True, null=True)