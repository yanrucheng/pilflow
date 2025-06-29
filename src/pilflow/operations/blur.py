from PIL import ImageFilter
from ..core.operation import Operation

class BlurOperation(Operation):
    """
    Apply blur effect to the image.
    """
    
    def __init__(self, radius=2):
        """Initialize blur operation.
        
        Args:
            radius: Blur radius (default: 2)
        """
        super().__init__(radius=radius)
        self.radius = radius
    
    def apply(self, img_pack):
        """
        Apply blur effect to the image.
        
        Args:
            img_pack: ImgPack instance
            
        Returns:
            ImgPack: New instance with blurred image
        """
        blurred_img = img_pack.pil_img.filter(ImageFilter.GaussianBlur(radius=self.radius))
        
        context_updates = {
            'blur_applied': True,
            'blur_radius': self.radius
        }
        
        return img_pack.copy(new_img=blurred_img, **context_updates)

# Register the operation
BlurOperation.register('blur')