from PIL import Image, ImageFilter

from pilflow import ImgPack
from pilflow.operations.sharpen import SharpenOperation


class TestSharpenOperation:
    """Tests for the SharpenOperation class."""
    
    def test_registration(self):
        """Test that the operation is registered with ImgPack."""
        assert 'sharpen' in ImgPack._operations
        assert ImgPack._operations['sharpen'] is SharpenOperation
    
    def test_init(self):
        """Test initialization with different parameters."""
        # Test with default parameters
        op = SharpenOperation()
        assert op.radius == 2
        assert op.percent == 150
        assert op.threshold == 3
        
        # Test with custom parameters
        op = SharpenOperation(radius=3, percent=200, threshold=5)
        assert op.radius == 3
        assert op.percent == 200
        assert op.threshold == 5
    
    def test_apply(self):
        """Test applying the sharpen operation."""
        # Create a test image
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Apply the operation with default parameters
        op = SharpenOperation()
        result = op.apply(img_pack)
        
        # Check the result
        assert result is not img_pack  # Should be a new instance
        assert result.pil_img is not img_pack.pil_img  # Should be a new image
        sharpen_context = result.get_context('sharpen')
        assert sharpen_context.sharpen_applied is True
        assert sharpen_context.sharpen_radius == 2
        assert sharpen_context.sharpen_percent == 150
        assert sharpen_context.sharpen_threshold == 3
        
        # Apply the operation with custom parameters
        op = SharpenOperation(radius=3, percent=200, threshold=5)
        result = op.apply(img_pack)
        
        # Check the result
        sharpen_context = result.get_context('sharpen')
        assert sharpen_context.sharpen_radius == 3
        assert sharpen_context.sharpen_percent == 200
        assert sharpen_context.sharpen_threshold == 5
    
    def test_method_chaining(self):
        """Test that the operation can be called via method chaining."""
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Test chaining
        result = img_pack.sharpen(radius=3, percent=200, threshold=5)
        
        sharpen_context = result.get_context('sharpen')
        assert sharpen_context.sharpen_applied is True
        assert sharpen_context.sharpen_radius == 3
        assert sharpen_context.sharpen_percent == 200
        assert sharpen_context.sharpen_threshold == 5
        assert isinstance(result.pil_img, Image.Image)