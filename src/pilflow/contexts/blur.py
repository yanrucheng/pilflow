from typing import Union
from ..core.context import ContextData


class BlurContextData(ContextData):
    """Context data for image blur information.
    
    This class stores information about blur operations applied to images,
    including blur radius and application status.
    """
    
    def __init__(self, blur_applied: bool, blur_radius: Union[int, float], **kwargs):
        """Initialize blur context data.
        
        Args:
            blur_applied: Whether blur has been applied to the image
            blur_radius: Radius of the blur effect
            **kwargs: Additional context data
        """
        super().__init__(
            blur_applied=blur_applied,
            blur_radius=blur_radius,
            **kwargs
        )
    
    def validate(self) -> None:
        """Validate blur context data.
        
        Raises:
            ValueError: If the data is invalid
        """
        blur_applied = self._data.get('blur_applied')
        blur_radius = self._data.get('blur_radius')
        
        if not isinstance(blur_applied, bool):
            raise ValueError("blur_applied must be a boolean")
        
        if not isinstance(blur_radius, (int, float)) or blur_radius < 0:
            raise ValueError("blur_radius must be a non-negative number")
        
        # If blur is applied, radius should be positive
        if blur_applied and blur_radius <= 0:
            raise ValueError("blur_radius must be positive when blur_applied is True")
    
    @property
    def blur_applied(self) -> bool:
        """Check if blur has been applied."""
        return self._data['blur_applied']
    
    @property
    def blur_radius(self) -> Union[int, float]:
        """Get blur radius."""
        return self._data['blur_radius']
    
    def is_light_blur(self) -> bool:
        """Check if this is a light blur (radius <= 2)."""
        return self.blur_applied and self.blur_radius <= 2
    
    def is_medium_blur(self) -> bool:
        """Check if this is a medium blur (2 < radius <= 5)."""
        return self.blur_applied and 2 < self.blur_radius <= 5
    
    def is_heavy_blur(self) -> bool:
        """Check if this is a heavy blur (radius > 5)."""
        return self.blur_applied and self.blur_radius > 5
    
    def get_blur_intensity(self) -> str:
        """Get blur intensity as a string.
        
        Returns:
            String describing blur intensity: 'none', 'light', 'medium', or 'heavy'
        """
        if not self.blur_applied:
            return 'none'
        elif self.is_light_blur():
            return 'light'
        elif self.is_medium_blur():
            return 'medium'
        else:
            return 'heavy'