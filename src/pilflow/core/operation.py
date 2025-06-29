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
    def register(cls, name_or_class=None):
        """Register this operation with ImgPack.
        
        Can be used as:
        1. @Operation.register - infers name from class name
        2. @Operation.register('custom_name') - uses provided name
        3. MyOperation.register() - manual registration
        4. MyOperation.register('custom_name') - manual registration with name
        
        Args:
            name_or_class: Either a name string or a class (when used as decorator)
        """
        from .image_pack import ImgPack
        
        def _register_operation(operation_class, operation_name=None):
            """Helper function to register an operation."""
            if operation_name is None:
                # Infer name from class name
                operation_name = operation_class.__name__.lower().replace('operation', '')
            ImgPack.register_operation(operation_name, operation_class)
            return operation_class
        
        # Case 1: Used as @Operation.register (no arguments)
        if name_or_class is None:
            # Return a decorator function
            return lambda operation_class: _register_operation(operation_class)
        
        # Case 2: Used as @Operation.register('name') or called with string
        elif isinstance(name_or_class, str):
            # Always return a decorator function when string is provided
            return lambda operation_class: _register_operation(operation_class, name_or_class)
        
        # Case 3: Used as decorator without parentheses @Operation.register
        # where name_or_class is actually the class being decorated
        else:
            # Direct registration of the class
            return _register_operation(name_or_class)