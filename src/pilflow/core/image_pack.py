from PIL import Image
from typing import Dict, Any, Optional, Union
from .context import ContextData
import json

class ImgPack:
    """Base class for image processing pipeline with structured context support."""
    
    # Registry for operations
    _operations = {}
    
    def __init__(self, pil_img, context_data=None):
        self.pil_img = pil_img
        self._context_data = context_data if context_data is not None else {}
        self._structured_contexts: Dict[str, ContextData] = {}

    @property
    def context(self):
        """Return the context data dictionary."""
        return self._context_data
    
    @property
    def img(self):
        """Return the PIL image object."""
        return self.pil_img
    
    def copy(self, new_img=None, **context_updates) -> 'ImgPack':
        """Create a new ImgPack instance with optional updates.
         
         Args:
             new_img: Optional new PIL image to use
             **context_updates: Additional context data to update
             
         Returns:
             ImgPack: A new ImgPack instance with copied image and context data.
         """
        img = new_img if new_img is not None else self.pil_img
        new_context = self._context_data.copy()
        new_context.update(context_updates)
        new_pack = ImgPack(img, new_context)
        # Deep copy structured contexts
        new_pack._structured_contexts = {}
        for name, context in self._structured_contexts.items():
            # Create a new instance from the context's data
            context_class = type(context)
            new_pack._structured_contexts[name] = context_class.from_dict(context.to_dict())
        return new_pack
    
    def add_context(self, context_data: ContextData, name: Optional[str] = None) -> None:
        """Add structured context data to the image pack.
        
        Args:
            context_data: ContextData instance to add
            name: Optional name for the context (inferred from class if not provided)
        """
        if name is None:
            # Infer name from context class registration
            context_class = type(context_data)
            for registered_name, registered_class in ContextData.get_registered_classes().items():
                if registered_class == context_class:
                    name = registered_name
                    break
            else:
                # Fallback to class name if not registered
                name = context_class.__name__.lower().replace('contextdata', '')
        
        self._structured_contexts[name] = context_data
        # Also update legacy context data
        self._context_data.update(context_data.to_dict())
    
    def get_context(self, name: str) -> Optional[ContextData]:
        """Get structured context data by name.
        
        Args:
            name: Name of the context data
            
        Returns:
            ContextData instance or None if not found
        """
        return self._structured_contexts.get(name)
    
    def has_context(self, name: str) -> bool:
        """Check if structured context data exists.
        
        Args:
            name: Name of the context data
            
        Returns:
            True if context exists, False otherwise
        """
        return name in self._structured_contexts
    
    def remove_context(self, name: str) -> bool:
        """Remove structured context data.
        
        Args:
            name: Name of the context data to remove
            
        Returns:
            True if context was removed, False if it didn't exist
        """
        if name in self._structured_contexts:
            del self._structured_contexts[name]
            return True
        return False
    
    def get_all_contexts(self) -> Dict[str, ContextData]:
        """Get all structured context data.
        
        Returns:
            Dictionary of all structured contexts
        """
        return self._structured_contexts.copy()
    
    def to_json(self, include_image_data: bool = False) -> str:
        """Convert ImgPack to JSON string.
        
        Args:
            include_image_data: Whether to include base64-encoded image data
            
        Returns:
            JSON string representation
        """
        data = {
            'context_data': self._context_data,
            'structured_contexts': {
                name: context.to_dict() 
                for name, context in self._structured_contexts.items()
            }
        }
        
        if include_image_data:
            import base64
            import io
            buffer = io.BytesIO()
            self.pil_img.save(buffer, format='PNG')
            img_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            data['image_data'] = img_data
            data['image_format'] = 'PNG'
        
        return json.dumps(data, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str, pil_img=None) -> 'ImgPack':
        """Create ImgPack from JSON string.
        
        Args:
            json_str: JSON string containing ImgPack data
            pil_img: PIL Image object (required if image_data not in JSON)
            
        Returns:
            ImgPack instance
        """
        data = json.loads(json_str)
        
        # Handle image data
        if 'image_data' in data and pil_img is None:
            import base64
            import io
            img_data = base64.b64decode(data['image_data'])
            pil_img = Image.open(io.BytesIO(img_data))
        elif pil_img is None:
            raise ValueError("Either provide pil_img parameter or include image_data in JSON")
        
        # Create ImgPack with legacy context data
        img_pack = cls(pil_img, data.get('context_data', {}))
        
        # Restore structured contexts
        structured_contexts = data.get('structured_contexts', {})
        for name, context_dict in structured_contexts.items():
            context_class = ContextData.get_context_class(name)
            if context_class:
                context_data = context_class.from_dict(context_dict)
                img_pack._structured_contexts[name] = context_data
        
        return img_pack
    
    def get_missing_contexts(self, required_contexts: list) -> list:
        """Get list of missing required contexts for logging purposes.
        
        Args:
            required_contexts: List of required context names
            
        Returns:
            List of missing context names
        """
        missing = []
        for context_name in required_contexts:
            if not self.has_context(context_name):
                missing.append(context_name)
        return missing
    
    def log_missing_contexts(self, required_contexts: list, operation_name: str = "operation") -> None:
        """Log missing contexts and suggest generator operations.
        
        Args:
            required_contexts: List of required context names
            operation_name: Name of the operation requiring contexts
        """
        missing = self.get_missing_contexts(required_contexts)
        if missing:
            print(f"Warning: {operation_name} requires missing contexts: {missing}")
            
            # Suggest producer operations based on registered producers
            suggestions = []
            for context_name in missing:
                producer_operations = ContextData.get_producer_operations(context_name)
                if producer_operations:
                    for producer_op in producer_operations:
                        suggestions.append(f"  - Run '{producer_op}' operation to generate '{context_name}' context")
                else:
                    # Fallback to heuristic approach if no producers registered
                    context_class = ContextData.get_context_class(context_name)
                    if context_class:
                        for op_name, op_class in self._operations.items():
                            if (context_name in op_name.lower() or 
                                (hasattr(op_class, '__doc__') and op_class.__doc__ and 
                                 context_name in op_class.__doc__.lower())):
                                suggestions.append(f"  - Run '{op_name}' operation to generate '{context_name}' context (heuristic)")
            
            if suggestions:
                print("Suggested operations to generate missing contexts:")
                for suggestion in suggestions:
                    print(suggestion)
    
    @classmethod
    def register_operation(cls, name, operation_class):
        """Register an operation class."""
        cls._operations[name] = operation_class
    
    def __getattr__(self, name):
        """Dynamically create operation methods."""
        if name in self._operations:
            operation_class = self._operations[name]
            def operation_method(*args, **kwargs):
                operation = operation_class(*args, **kwargs)
                return operation(self)
            return operation_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

def from_file(file_path):
    try:
        pil_img = Image.open(file_path)
        return ImgPack(pil_img, context_data={})
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None