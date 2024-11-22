
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *
from PIL import Image 
class ImageMap(BaseModelImpl):
    pro = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                            related_name="pro_image_maps", null=True, blank=True)
    image = models.ImageField(upload_to='folder_image_maps/', null=True, blank=True)
    original_width = models.PositiveIntegerField(null=True, blank=True)
    original_height = models.PositiveIntegerField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_image_maps")
   
        
    def __str__(self):
        return self.name
    
    def save_image_map(instance):
        if instance.image and (not instance.original_width or not instance.original_height):
            with Image.open(instance.image.path) as img:
                instance.original_width, instance.original_height = img.size

class ImageMapArea(BaseModelTrackImpl):
    image_map = models.ForeignKey(ImageMap, related_name='areas', on_delete=models.CASCADE, null=True, blank=True)
    shape = models.CharField(max_length=20, choices=[('rect', 'Rectangle'), ('circle', 'Circle'), ('poly', 'Polygon')], null=True, blank=True)
    coords = models.TextField(help_text="Comma-separated coordinates (e.g., x1,y1,x2,y2)", null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    hover_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Area for {self.image_map.name}"