from PIL import Image
from ..core.operation import Operation
from ..contexts.resize import ResizeContextData

@ResizeContextData.register_as_producer
@Operation.register
class ResizeOperation(Operation):
    """
    Resize the image based on context or provided dimensions.
    """
    
    def __init__(self, width=None, height=None, resolution_preset=None):
        """Initialize resize operation with target dimensions or resolution preset.
        
        Args:
            width: Target width (optional)
            height: Target height (optional)
            resolution_preset: ResolutionPreset enum value (optional)
        """
        super().__init__(width=width, height=height, resolution_preset=resolution_preset)
        self.width = width
        self.height = height
        self.resolution_preset = resolution_preset
    
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
        
        # If resolution_preset is provided directly, use it
        if self.resolution_preset is not None:
            target_width, target_height = self.resolution_preset.value
            
            # Handle ORIGINAL preset (None, None)
            if target_width is None or target_height is None:
                width = current_img.width
                height = current_img.height
            else:
                width = target_width
                height = target_height
        
        # If no dimensions provided, try to use context
        if width is None and height is None:
            # Check for resolution decision context
            resolution_decision_context = img_pack.get_context('resolution_decision')
            if resolution_decision_context:
                # Extract width and height from the resolution preset
                target_width, target_height = resolution_decision_context.resolution_preset.value
                
                # Handle ORIGINAL preset (None, None)
                if target_width is None or target_height is None:
                    width = current_img.width
                    height = current_img.height
                else:
                    width = target_width
                    height = target_height
            else:
                # Check if there are target dimensions in legacy context
                width = context.get('target_width')
                height = context.get('target_height')
            
            # If still no dimensions, use a default resize strategy
            if width is None and height is None:
                # Fallback to image dimensions
                original_width = current_img.width
                original_height = current_img.height
                aspect_ratio = original_width / original_height
                
                # Default: resize to HD if larger than HD
                if original_width > 1280 or original_height > 720:
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
        
        # Create structured resize context data
        resize_context = ResizeContextData(
            current_width=width,
            current_height=height,
            resized=True,
            resize_width=width,
            resize_height=height,
            target_width=self.width,
            target_height=self.height
        )
        
        # Create new img_pack with structured context
        new_pack = img_pack.copy(new_img=resized_img)
        new_pack.add_context(resize_context)
        
        return new_pack