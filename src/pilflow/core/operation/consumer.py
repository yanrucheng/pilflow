from abc import abstractmethod
from .base import BaseOperation


class Consumer(BaseOperation):
    """Base class for consumers (ImgPack input, any output)."""
    
    @abstractmethod
    def apply(self, img_pack):
        """Consume an ImgPack and return processed data.
        
        Args:
            img_pack: ImgPack instance to process
            
        Returns:
            Any: Processed output data
        """
        pass