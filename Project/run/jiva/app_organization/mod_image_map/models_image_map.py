
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *
from PIL import Image 
from lxml import etree
class ImageMap(BaseModelImpl):
    pro = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                            related_name="pro_image_maps", null=True, blank=True)
    image = models.FileField(upload_to='folder_image_maps/', null=True, blank=True)
    original_width = models.PositiveIntegerField(null=True, blank=True)
    original_height = models.PositiveIntegerField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_image_maps")
   
        
    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        # Save the instance first to ensure the file is available on disk
        super().save(*args, **kwargs)

        # Check if the image exists
        if self.image:
            try:
                # Handle SVG files
                if self.image.name.lower().endswith('.svg'):
                    with open(self.image.path, 'rb') as svg_file:
                        tree = etree.parse(svg_file)
                        root = tree.getroot()
                        print(f">>> === SVG Root Attributes: {root.attrib} === <<<")
                        # Extract width and height attributes
                        width = root.attrib.get('width')
                        height = root.attrib.get('height')
                        print(f">>> === width: {width}, height: {height} === <<<")
                        if width != None  and height != None:
                            self.original_width = int(float(width.replace('px', '')))
                            self.original_height = int(float(height.replace('px', '')))
                        else:
                            # Fallback to viewBox if width/height are not defined
                            viewBox = root.attrib.get('viewBox')
                            if viewBox:
                                _, _, w, h = map(float, viewBox.split())
                                self.original_width = int(w)
                                self.original_height = int(h)
                                print(f">>> === VIEWBOX width: {w}, height: {h} === <<<")
                            else:
                                # Log a warning and use default dimensions
                                print(">>> WARNING: SVG has no width, height, or viewBox. Assigning default dimensions. <<<")
                                self.original_width = 800
                                self.original_height = 600

                # Handle raster images (JPEG, PNG, etc.)
                else:
                    with Image.open(self.image.path) as img:
                        self.original_width, self.original_height = img.size

                # Save the instance again to store dimensions
                print(f">>> About to save: original_width={self.original_width}, original_height={self.original_height} <<<")
                super().save(update_fields=['original_width', 'original_height'])
                print(f">>> Saved: original_width={self.original_width}, original_height={self.original_height} <<<")

            except Exception as e:
                print(f"Error processing image dimensions: {e}")

class ImageMapAreaProject(BaseModelTrackImpl):
    image_map = models.ForeignKey(ImageMap, related_name='areas', on_delete=models.CASCADE, null=True, blank=True)
    shape = models.CharField(max_length=20, choices=[('rect', 'Rectangle'), ('circle', 'Circle'), ('poly', 'Polygon')], null=True, blank=True)
    coords = models.TextField(help_text="Comma-separated coordinates (e.g., x1,y1,x2,y2)", null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    hover_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Area for {self.image_map.name}"