from abc import abstractmethod
from .base import BaseOperation


class Operation(BaseOperation):
    """Base class for image processing operations (ImgPack in, ImgPack out)."""
    
    @abstractmethod
    def apply(self, img_pack):
        """Apply the operation to an ImgPack and return a new ImgPack.
        
        Args:
            img_pack: ImgPack instance to process
            
        Returns:
            ImgPack: New ImgPack instance with operation applied
        """
        pass

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
        from ..image_pack import ImgPack
        
        def _register_operation(operation_class, operation_name=None):
            """Helper function to register an operation."""
            if operation_name is None:
                operation_name = BaseOperation._get_operation_name(operation_class)
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