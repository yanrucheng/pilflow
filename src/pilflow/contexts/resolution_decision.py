from typing import Union
from ..core.context import ContextData


class ResolutionDecisionContextData(ContextData):
    """Context data for resolution decision operations.
    
    This context stores the target resolution preset
    for use by resize operations.
    """
    
    def __init__(self, resolution_preset):
        """Initialize resolution decision context data.
        
        Args:
            resolution_preset: ResolutionPreset enum value
        """
        super().__init__(
            resolution_preset=resolution_preset
        )
    
    def validate(self) -> None:
        """Validate the resolution decision context data.
        
        Raises:
            ValueError: If resolution_preset is None or invalid
        """
        resolution_preset = self._data.get('resolution_preset')
        
        if resolution_preset is None:
            raise ValueError("resolution_preset cannot be None")
        
        if not hasattr(resolution_preset, 'value'):
            raise ValueError("resolution_preset must be a ResolutionPreset enum")
    
    @property
    def resolution_preset(self):
        """Get the resolution preset.
        
        Returns:
            ResolutionPreset: The resolution preset enum value
        """
        return self._data['resolution_preset']
    
    def to_dict(self) -> dict:
        """Convert to dictionary with enum serialization.
        
        Returns:
            dict: Dictionary representation with serializable values
        """
        data = self._data.copy()
        # Convert ResolutionPreset enum to its name for JSON serialization
        if 'resolution_preset' in data:
            data['resolution_preset'] = data['resolution_preset'].name
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary with enum deserialization.
        
        Args:
            data: Dictionary containing context data
            
        Returns:
            ResolutionDecisionContextData: New instance
        """
        from jinnang.media.resolution import ResolutionPreset
        
        # Convert string back to ResolutionPreset enum
        if 'resolution_preset' in data and isinstance(data['resolution_preset'], str):
            data = data.copy()
            data['resolution_preset'] = ResolutionPreset[data['resolution_preset']]
        
        return cls(resolution_preset=data['resolution_preset'])