from abc import ABC, abstractmethod
import re


class BaseOperation(ABC):
    """Base class for all operations in the pipeline."""
    
    def __init__(self, *args, **kwargs):
        """Initialize operation with parameters."""
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self, *args, **kwargs):
        """Make operation callable."""
        return self.apply(*args, **kwargs)
    
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
        
        # Remove common suffixes
        for suffix in ['_operation', '_producer', '_consumer']:
            if name.endswith(suffix):
                return name[:-len(suffix)]
        return name