from typing import Union
from ..core.context import ContextData


@ContextData.register
class ResolutionContextData(ContextData):
    """Context data for image resolution information.
    
    This class stores information about image resolution, dimensions,
    and aspect ratio in a structured, JSON-serializable format.
    """
    
    def __init__(self, original_width: int, original_height: int, 
                 resolution_category: str, aspect_ratio: float, **kwargs):
        """Initialize resolution context data.
        
        Args:
            original_width: Original image width in pixels
            original_height: Original image height in pixels
            resolution_category: Category like '4K', 'Full HD', 'HD', 'SD'
            aspect_ratio: Width/height ratio
            **kwargs: Additional context data
        """
        super().__init__(
            original_width=original_width,
            original_height=original_height,
            resolution_category=resolution_category,
            aspect_ratio=aspect_ratio,
            **kwargs
        )
    
    def validate(self) -> None:
        """Validate resolution context data.
        
        Raises:
            ValueError: If the data is invalid
        """
        width = self._data.get('original_width')
        height = self._data.get('original_height')
        category = self._data.get('resolution_category')
        aspect_ratio = self._data.get('aspect_ratio')
        
        if not isinstance(width, int) or width <= 0:
            raise ValueError("original_width must be a positive integer")
        
        if not isinstance(height, int) or height <= 0:
            raise ValueError("original_height must be a positive integer")
        
        if category not in ['4K', 'Full HD', 'HD', 'SD']:
            raise ValueError("resolution_category must be one of: '4K', 'Full HD', 'HD', 'SD'")
        
        if not isinstance(aspect_ratio, (int, float)) or aspect_ratio <= 0:
            raise ValueError("aspect_ratio must be a positive number")
        
        # Validate aspect ratio matches dimensions
        calculated_ratio = width / height
        if abs(calculated_ratio - aspect_ratio) > 0.01:  # Allow small floating point errors
            raise ValueError(f"aspect_ratio {aspect_ratio} doesn't match dimensions {width}x{height}")
    
    @property
    def original_width(self) -> int:
        """Get original image width."""
        return self._data['original_width']
    
    @property
    def original_height(self) -> int:
        """Get original image height."""
        return self._data['original_height']
    
    @property
    def resolution_category(self) -> str:
        """Get resolution category."""
        return self._data['resolution_category']
    
    @property
    def aspect_ratio(self) -> float:
        """Get aspect ratio."""
        return self._data['aspect_ratio']
    
    @property
    def total_pixels(self) -> int:
        """Calculate total number of pixels."""
        return self.original_width * self.original_height
    
    def is_4k(self) -> bool:
        """Check if image is 4K resolution."""
        return self.resolution_category == '4K'
    
    def is_hd_or_better(self) -> bool:
        """Check if image is HD resolution or better."""
        return self.resolution_category in ['4K', 'Full HD', 'HD']
    
    def is_landscape(self) -> bool:
        """Check if image is in landscape orientation."""
        return self.aspect_ratio > 1.0
    
    def is_portrait(self) -> bool:
        """Check if image is in portrait orientation."""
        return self.aspect_ratio < 1.0
    
    def is_square(self) -> bool:
        """Check if image is square (within tolerance)."""
        return abs(self.aspect_ratio - 1.0) < 0.01