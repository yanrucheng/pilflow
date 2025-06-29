from PIL import Image

class ImgPack:
    """Base class for image processing pipeline."""
    
    # Registry for operations
    _operations = {}
    
    def __init__(self, pil_img, context_data=None):
        self.pil_img = pil_img
        self._context_data = context_data if context_data is not None else {}

    @property
    def context(self):
        """Return the context data dictionary."""
        return self._context_data
    
    @property
    def img(self):
        """Return the PIL image object."""
        return self.pil_img
    
    def copy(self, new_img=None, **context_updates):
        """Create a new ImgPack instance with optional updates."""
        img = new_img if new_img is not None else self.pil_img
        new_context = self._context_data.copy()
        new_context.update(context_updates)
        return ImgPack(img, new_context)
    
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