from PIL import Image
from ..core.operation import Operation

@Operation.register('resize')
class ResizeOperation(Operation):
    """
    Resize the image based on context or provided dimensions.
    """
    
    def __init__(self, width=None, height=None):
        """Initialize resize operation with target dimensions.
        
        Args:
            width: Target width (optional)
            height: Target height (optional)
        """
        super().__init__(width=width, height=height)
        self.width = width
        self.height = height
    
    def apply(self, img_pack):
        """
        Resize the image based on context or provided dimensions.
        
        Args:
            img_pack: ImgPack instance
            
        Returns:
            ImgPack: New instance with resized image
        """
        current_img = img_pack.pil_img
        context = img_pack.context
        width = self.width
        height = self.height
        
        # If no dimensions provided, try to use context
        if width is None and height is None:
            # Check if there are target dimensions in context
            width = context.get('target_width')
            height = context.get('target_height')
            
            # If still no dimensions, use a default resize strategy
            if width is None and height is None:
                # Default: resize to HD if larger than HD
                original_width = context.get('original_width', current_img.width)
                original_height = context.get('original_height', current_img.height)
                
                if original_width > 1280 or original_height > 720:
                    aspect_ratio = context.get('aspect_ratio', original_width / original_height)
                    if aspect_ratio >= 16/9:  # Wide aspect ratio
                        width = 1280
                        height = int(1280 / aspect_ratio)
                    else:  # Tall aspect ratio
                        height = 720
                        width = int(720 * aspect_ratio)
                else:
                    # Image is already small enough, no resize needed
                    return img_pack.copy()
        
        # Calculate missing dimension while preserving aspect ratio
        if width is None and height is not None:
            aspect_ratio = current_img.width / current_img.height
            width = int(height * aspect_ratio)
        elif height is None and width is not None:
            aspect_ratio = current_img.width / current_img.height
            height = int(width / aspect_ratio)
        
        # Resize the image
        resized_img = current_img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Update context with new dimensions
        context_updates = {
            'current_width': width,
            'current_height': height,
            'resize_width': width,
            'resize_height': height,
            'resized': True
        }
        
        return img_pack.copy(new_img=resized_img, **context_updates)