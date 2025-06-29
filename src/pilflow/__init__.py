from .core.image_pack import ImgPack
from .core.operation import Operation
from .core.context import ContextData

# Import context classes to register them
from . import contexts

# Import operations to trigger registration
from . import operations

__version__ = "0.1.0"
__all__ = ["ImgPack", "Operation"]