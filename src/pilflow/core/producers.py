import base64
import binascii
from io import BytesIO
from PIL import Image
import PIL
from .operation import Producer

class FromFileProducer(Producer):
    """Producer that creates ImgPack from image file."""
    
    def __init__(self, file_path: str, **kwargs):
        """Initialize file producer.
        
        Args:
            file_path: Path to the image file
            **kwargs: Additional context data to initialize the ImgPack
        """
        super().__init__(file_path=file_path, **kwargs)
        self.file_path = file_path
        self.context_kwargs = kwargs
    
    def apply(self):
        """Create an ImgPack instance from an image file.
        
        Returns:
            ImgPack: A new ImgPack instance
            
        Raises:
            FileNotFoundError: If the file does not exist
            PIL.UnidentifiedImageError: If the file is not a valid image
        """
        from .image_pack import ImgPack
        
        try:
            pil_img = Image.open(self.file_path)
            return ImgPack(pil_img, context_data=self.context_kwargs)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Image file not found: {self.file_path}")
        except PIL.UnidentifiedImageError as e:
            raise PIL.UnidentifiedImageError(f"File is not a valid image: {self.file_path}")

class FromBase64Producer(Producer):
    """Producer that creates ImgPack from base64 string."""
    
    def __init__(self, base64_string: str, **kwargs):
        """Initialize base64 producer.
        
        Args:
            base64_string: The base64 encoded string of the image
            **kwargs: Additional context data to initialize the ImgPack
        """
        super().__init__(base64_string=base64_string, **kwargs)
        self.base64_string = base64_string
        self.context_kwargs = kwargs
    
    def apply(self):
        """Create an ImgPack instance from a base64 encoded string.
        
        Returns:
            ImgPack: A new ImgPack instance
            
        Raises:
            ValueError: If the base64 string is invalid or cannot be decoded
            PIL.UnidentifiedImageError: If the decoded data is not a valid image
        """
        from .image_pack import ImgPack
        
        try:
            image_data = base64.b64decode(self.base64_string)
            pil_img = Image.open(BytesIO(image_data))
            return ImgPack(pil_img, context_data=self.context_kwargs)
        except (binascii.Error, ValueError) as e:
            raise ValueError(f"Invalid base64 string: {str(e)}")
        except PIL.UnidentifiedImageError as e:
            raise PIL.UnidentifiedImageError(f"Decoded data is not a valid image: {str(e)}")