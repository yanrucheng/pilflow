import json
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Set
from .operation import BaseOperation


class ContextData(ABC):
    """Base class for all context data classes.
    
    All context data classes must be JSON serializable and provide
    a clear interface for data access and validation.
    """
    
    # Registry for operations that produce each context type
    _producer_operations: Dict[str, Set[str]] = {}
    
    def __init__(self, **kwargs):
        """Initialize context data with keyword arguments."""
        self._data = kwargs
        self.validate()
    
    @abstractmethod
    def validate(self) -> None:
        """Validate the context data.
        
        Raises:
            ValueError: If the data is invalid
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context data to dictionary for JSON serialization.
        
        Returns:
            Dict containing all context data
        """
        return self._data.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextData':
        """Create context data instance from dictionary.
        
        Args:
            data: Dictionary containing context data
            
        Returns:
            ContextData instance
        """
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert context data to JSON string.
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ContextData':
        """Create context data instance from JSON string.
        
        Args:
            json_str: JSON string containing context data
            
        Returns:
            ContextData instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from context data.
        
        Args:
            key: Key to retrieve
            default: Default value if key not found
            
        Returns:
            Value associated with key or default
        """
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set value in context data.
        
        Args:
            key: Key to set
            value: Value to set
        """
        self._data[key] = value
        self.validate()
    
    def update(self, **kwargs) -> None:
        """Update context data with new values.
        
        Args:
            **kwargs: Key-value pairs to update
        """
        self._data.update(kwargs)
        self.validate()
    
    @classmethod
    def _get_context_name(cls):
        """Get the context name from the class name.
        
        Returns:
            str: The context name in snake_case
        """
        name = cls.__name__
        name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
        name = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', name).lower()
        
        if name.endswith('_context_data'):
            return name[:-len('_context_data')]
        elif name.endswith('_context'):
            return name[:-len('_context')]
        else:
            return name
    
    @classmethod
    def register_as_producer(cls, operation_class=None):
        """Decorator to register an operation as a producer of this context type.
        
        Usage:
        @ResolutionDecisionContextData.register_as_producer
        @Operation.register
        class DecideResolutionOperation(Operation):
            ...
            
        Returns:
            Decorator function or decorated class
        """
        def decorator(op_class):
            # Get the operation name from the class
            # Import moved to top of file
            operation_name = BaseOperation._get_operation_name(op_class)
            
            # Get the context name from the current class
            context_name = cls._get_context_name()
            
            # Register this operation as a producer of the context
            cls.register_producer_operation(context_name, operation_name)
            
            return op_class
        
        # If called with a class directly (without parentheses)
        if operation_class is not None:
            return decorator(operation_class)
        
        # If called as @decorator (with parentheses)
        return decorator
    
    @classmethod
    def register_producer_operation(cls, context_name: str, operation_name: str) -> None:
        """Register an operation as a producer of a specific context type.
        
        Args:
            context_name: Name of the context type
            operation_name: Name of the operation that produces this context
        """
        if context_name not in cls._producer_operations:
            cls._producer_operations[context_name] = set()
        cls._producer_operations[context_name].add(operation_name)
    
    @classmethod
    def get_registered_classes(cls) -> Dict[str, Any]:
        """Get all registered context data classes.
        
        Note: Context classes no longer require registration.
        This method is kept for backward compatibility with tests.
        
        Returns:
            Empty dictionary (contexts don't need registration anymore)
        """
        return {}
    
    @classmethod
    def get_producer_operations(cls, context_name: str) -> Set[str]:
        """Get operations that produce a specific context type.
        
        Args:
            context_name: Name of the context type
            
        Returns:
            Set of operation names that produce this context
        """
        return cls._producer_operations.get(context_name, set())
    
    @classmethod
    def get_all_producer_operations(cls) -> Dict[str, Set[str]]:
        """Get all producer operations for all context types.
        
        Returns:
            Dictionary mapping context names to sets of producer operation names
        """
        return cls._producer_operations.copy()
     
    def __repr__(self) -> str:
        """String representation of context data."""
        return f"{self.__class__.__name__}({self._data})"
    
    def __eq__(self, other) -> bool:
        """Check equality with another context data instance."""
        if not isinstance(other, ContextData):
            return False
        return self._data == other._data