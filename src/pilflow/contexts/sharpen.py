from typing import Union
from ..core.context import ContextData


@ContextData.register
class SharpenContextData(ContextData):
    """Context data for image sharpen information.
    
    This class stores information about sharpen operations applied to images,
    including sharpen factor and application status.
    """
    
    def __init__(self, sharpen_applied: bool, sharpen_radius: Union[int, float], sharpen_percent: Union[int, float], sharpen_threshold: Union[int, float], **kwargs):
        """Initialize sharpen context data.
        
        Args:
            sharpen_applied: Whether sharpen has been applied to the image
            sharpen_radius: Radius of the sharpen effect
            sharpen_percent: Sharpening amount in percent
            sharpen_threshold: Minimum brightness difference to apply sharpening
            **kwargs: Additional context data
        """
        super().__init__(
            sharpen_applied=sharpen_applied,
            sharpen_radius=sharpen_radius,
            sharpen_percent=sharpen_percent,
            sharpen_threshold=sharpen_threshold,
            **kwargs
        )
    
    def validate(self) -> None:
        """Validate sharpen context data.
        
        Raises:
            ValueError: If the data is invalid
        """
        sharpen_applied = self._data.get('sharpen_applied')
        sharpen_radius = self._data.get('sharpen_radius')
        sharpen_percent = self._data.get('sharpen_percent')
        sharpen_threshold = self._data.get('sharpen_threshold')
        
        if not isinstance(sharpen_applied, bool):
            raise ValueError("sharpen_applied must be a boolean")
        
        if not isinstance(sharpen_radius, (int, float)) or sharpen_radius < 0:
            raise ValueError("sharpen_radius must be a non-negative number")
        
        if not isinstance(sharpen_percent, (int, float)) or sharpen_percent < 0:
            raise ValueError("sharpen_percent must be a non-negative number")
        
        if not isinstance(sharpen_threshold, (int, float)) or sharpen_threshold < 0:
            raise ValueError("sharpen_threshold must be a non-negative number")
        
        # If sharpen is applied, radius, percent, and threshold should be positive
        if sharpen_applied and (sharpen_radius <= 0 or sharpen_percent <= 0 or sharpen_threshold <= 0):
            raise ValueError("sharpen_radius, sharpen_percent, and sharpen_threshold must be positive when sharpen_applied is True")
    
    @property
    def sharpen_applied(self) -> bool:
        """Check if sharpen has been applied."""
        return self._data['sharpen_applied']
    
    @property
    def sharpen_radius(self) -> Union[int, float]:
        """Get the sharpen radius."""
        return self._data['sharpen_radius']
    
    @property
    def sharpen_percent(self) -> Union[int, float]:
        """Get the sharpen percent."""
        return self._data['sharpen_percent']
    
    @property
    def sharpen_threshold(self) -> Union[int, float]:
        """Get the sharpen threshold."""
        return self._data['sharpen_threshold']