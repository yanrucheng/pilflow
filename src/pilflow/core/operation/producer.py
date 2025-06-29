from abc import abstractmethod
from .base import BaseOperation


class Producer(BaseOperation):
    """Base class for producers (any input, ImgPack output)."""
    
    @abstractmethod
    def apply(self, *args, **kwargs):
        """Produce an ImgPack from input data.
        
        Args:
            *args, **kwargs: Input data and parameters
            
        Returns:
            ImgPack: New ImgPack instance
        """
        pass