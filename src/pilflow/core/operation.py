from abc import ABC, abstractmethod

class Operation(ABC):
    """Base class for all image processing operations."""
    
    def __init__(self, *args, **kwargs):
        """Initialize operation with parameters."""
        self.args = args
        self.kwargs = kwargs
    
    @abstractmethod
    def apply(self, img_pack):
        """Apply the operation to an ImgPack and return a new ImgPack.
        
        Args:
            img_pack: ImgPack instance to process
            
        Returns:
            ImgPack: New ImgPack instance with operation applied
        """
        pass
    
    def __call__(self, img_pack):
        """Make operation callable."""
        return self.apply(img_pack)
    
    @classmethod
    def register(cls, name=None):
        """Register this operation with ImgPack.
        
        Args:
            name: Optional name for the operation. If not provided, uses class name in lowercase.
        """
        from .image_pack import ImgPack
        
        operation_name = name or cls.__name__.lower().replace('operation', '')
        ImgPack.register_operation(operation_name, cls)
        return cls