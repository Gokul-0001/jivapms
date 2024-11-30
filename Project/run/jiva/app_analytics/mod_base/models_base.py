from app_jivapms.mod_app.all_model_imports import *
import uuid
class PageVisit(models.Model):
    visit_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Random UUID
    url = models.URLField(max_length=2048)
    visit_date = models.DateTimeField(auto_now_add=True)  # Date and time of the visit
    duration = models.DurationField(null=True, blank=True)  # Duration of the visit (optional)
    name = models.CharField(max_length=255, blank=True)  # Name of the visitor (optional)

    def __str__(self):
        return f"Visit to {self.url} on {self.visit_date}"
