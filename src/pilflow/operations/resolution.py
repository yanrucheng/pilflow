from ..core.operation import Operation
from ..contexts.resolution import ResolutionContextData

@Operation.register
class DecideResolutionOperation(Operation):
    """
    Analyze image resolution and add information to context.
    """
    
    def apply(self, img_pack):
        """
        Analyze image resolution and add information to context.
        
        Args:
            img_pack: ImgPack instance
            
        Returns:
            ImgPack: New instance with resolution info in context
        """
        width, height = img_pack.pil_img.size
        
        # Determine resolution category
        total_pixels = width * height
        if total_pixels >= 3840 * 2160:  # 4K
            resolution_category = "4K"
        elif total_pixels >= 1920 * 1080:  # Full HD
            resolution_category = "Full HD"
        elif total_pixels >= 1280 * 720:  # HD
            resolution_category = "HD"
        else:
            resolution_category = "SD"
        
        # Create structured resolution context data
        resolution_context = ResolutionContextData(
            original_width=width,
            original_height=height,
            resolution_category=resolution_category,
            aspect_ratio=width / height
        )
        
        # Create new img_pack with structured context
        new_pack = img_pack.copy()
        new_pack.add_context(resolution_context)
        
        return new_pack