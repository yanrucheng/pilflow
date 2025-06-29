import re
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
    
    @staticmethod
    def _get_operation_name(operation_class):
        """Get the operation name from a class.
        
        Args:
            operation_class: The operation class
            
        Returns:
            str: The operation name in snake_case
        """
        name = operation_class.__name__
        name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
        name = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', name).lower()
        
        if name.endswith('_operation'):
            return name[:-len('_operation')]
        else:
            return name
    
    @classmethod
    def register(cls, name_or_class=None):
        """Register this operation with ImgPack.
        
        Preferred usage:
        @Operation.register  # Infers name from class name (recommended)
        class MyOperation(Operation):
            ...
            
        Alternative usages:
        @Operation.register('custom_name')  # Explicit name
        MyOperation.register()  # Manual registration (for tests)
        
        Args:
            name_or_class: Either a name string or a class (when used as decorator)
        """
        from .image_pack import ImgPack
        
        def _register_operation(operation_class, operation_name=None):
            """Helper function to register an operation."""
            if operation_name is None:
                operation_name = cls._get_operation_name(operation_class)
            ImgPack.register_operation(operation_name, operation_class)
            return operation_class
        
        # Preferred case: @Operation.register (no arguments)
        if name_or_class is None:
            # Return a decorator function
            return lambda operation_class: _register_operation(operation_class)
        
        # Alternative case: @Operation.register('name') or called with string
        elif isinstance(name_or_class, str):
            # Return a decorator function when string is provided
            return lambda operation_class: _register_operation(operation_class, name_or_class)
        
        # Direct registration case (primarily for backward compatibility)
        else:
            # Direct registration of the class
            return _register_operation(name_or_class)