from typing import Optional
from ..core.context import ContextData


@ContextData.register
class ResizeContextData(ContextData):
    """Context data for image resize information.
    
    This class stores information about image resizing operations,
    target dimensions, and resize status in a structured format.
    """
    
    def __init__(self, current_width: int, current_height: int, 
                 resized: bool = False, target_width: Optional[int] = None,
                 target_height: Optional[int] = None, resize_width: Optional[int] = None,
                 resize_height: Optional[int] = None, **kwargs):
        """Initialize resize context data.
        
        Args:
            current_width: Current image width in pixels
            current_height: Current image height in pixels
            resized: Whether the image has been resized
            target_width: Target width for resizing (optional)
            target_height: Target height for resizing (optional)
            resize_width: Actual width after resize (optional)
            resize_height: Actual height after resize (optional)
            **kwargs: Additional context data
        """
        super().__init__(
            current_width=current_width,
            current_height=current_height,
            resized=resized,
            target_width=target_width,
            target_height=target_height,
            resize_width=resize_width,
            resize_height=resize_height,
            **kwargs
        )
    
    def validate(self) -> None:
        """Validate resize context data.
        
        Raises:
            ValueError: If the data is invalid
        """
        current_width = self._data.get('current_width')
        current_height = self._data.get('current_height')
        resized = self._data.get('resized', False)
        target_width = self._data.get('target_width')
        target_height = self._data.get('target_height')
        resize_width = self._data.get('resize_width')
        resize_height = self._data.get('resize_height')
        
        if not isinstance(current_width, int) or current_width <= 0:
            raise ValueError("current_width must be a positive integer")
        
        if not isinstance(current_height, int) or current_height <= 0:
            raise ValueError("current_height must be a positive integer")
        
        if not isinstance(resized, bool):
            raise ValueError("resized must be a boolean")
        
        # Validate optional target dimensions
        if target_width is not None and (not isinstance(target_width, int) or target_width <= 0):
            raise ValueError("target_width must be a positive integer or None")
        
        if target_height is not None and (not isinstance(target_height, int) or target_height <= 0):
            raise ValueError("target_height must be a positive integer or None")
        
        # Validate optional resize dimensions
        if resize_width is not None and (not isinstance(resize_width, int) or resize_width <= 0):
            raise ValueError("resize_width must be a positive integer or None")
        
        if resize_height is not None and (not isinstance(resize_height, int) or resize_height <= 0):
            raise ValueError("resize_height must be a positive integer or None")
        
        # If resized is True, resize dimensions should be provided
        if resized and (resize_width is None or resize_height is None):
            raise ValueError("resize_width and resize_height must be provided when resized is True")
    
    @property
    def current_width(self) -> int:
        """Get current image width."""
        return self._data['current_width']
    
    @property
    def current_height(self) -> int:
        """Get current image height."""
        return self._data['current_height']
    
    @property
    def resized(self) -> bool:
        """Check if image has been resized."""
        return self._data.get('resized', False)
    
    @property
    def target_width(self) -> Optional[int]:
        """Get target width for resizing."""
        return self._data.get('target_width')
    
    @property
    def target_height(self) -> Optional[int]:
        """Get target height for resizing."""
        return self._data.get('target_height')
    
    @property
    def resize_width(self) -> Optional[int]:
        """Get actual width after resize."""
        return self._data.get('resize_width')
    
    @property
    def resize_height(self) -> Optional[int]:
        """Get actual height after resize."""
        return self._data.get('resize_height')
    
    @property
    def current_aspect_ratio(self) -> float:
        """Calculate current aspect ratio."""
        return self.current_width / self.current_height
    
    @property
    def target_aspect_ratio(self) -> Optional[float]:
        """Calculate target aspect ratio if target dimensions are set."""
        if self.target_width and self.target_height:
            return self.target_width / self.target_height
        return None
    
    @property
    def resize_aspect_ratio(self) -> Optional[float]:
        """Calculate resize aspect ratio if resize dimensions are set."""
        if self.resize_width and self.resize_height:
            return self.resize_width / self.resize_height
        return None
    
    def has_target_dimensions(self) -> bool:
        """Check if target dimensions are set."""
        return self.target_width is not None and self.target_height is not None
    
    def calculate_scale_factor(self) -> Optional[float]:
        """Calculate scale factor if resize was performed."""
        if not self.resized or not self.resize_width or not self.resize_height:
            return None
        
        # Use width scale factor (should be same as height for proportional scaling)
        return self.resize_width / self.current_width