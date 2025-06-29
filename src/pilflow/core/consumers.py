import base64
from io import BytesIO
from .operation import Consumer

@Consumer.register
class ToBase64Consumer(Consumer):
    """Consumer that converts ImgPack to base64 string."""
    
    def __init__(self, format="PNG"):
        """Initialize base64 consumer.
        
        Args:
            format: Image format for encoding (default: PNG)
        """
        super().__init__(format=format)
        self.format = format
    
    def apply(self, img_pack):
        """Convert ImgPack to base64 string.
        
        Args:
            img_pack: ImgPack instance to convert
            
        Returns:
            str: Base64 encoded string of the image
        """
        buffered = BytesIO()
        img_pack.pil_img.save(buffered, format=self.format)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

@Consumer.register
class ToImageConsumer(Consumer):
    """Consumer that extracts PIL Image from ImgPack."""
    
    def apply(self, img_pack):
        """Extract PIL Image from ImgPack.
        
        Args:
            img_pack: ImgPack instance
            
        Returns:
            PIL.Image: The PIL image object
        """
        return img_pack.pil_img