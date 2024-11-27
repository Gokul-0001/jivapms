
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from django.utils.text import slugify
import uuid
class Blog(BaseModelImpl):
    organization = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="organization_blogs", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_blogs")
   
        
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate a slug only if it doesn't exist
            base_slug = slugify(self.name) if self.name else str(uuid.uuid4())
            unique_slug = base_slug
            num = 1
            while Blog.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else str(self.id)
