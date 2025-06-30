import pytest
from PIL import Image, ImageFilter

from pilflow import ImgPack
from pilflow.operations.blur import BlurOperation


class TestBlurOperation:
    """Tests for the BlurOperation class."""
    
    def test_registration(self):
        """Test that the operation is registered with ImgPack."""
        assert 'blur' in ImgPack._operations
        assert ImgPack._operations['blur'] is BlurOperation
    
    def test_init(self):
        """Test initialization with different parameters."""
        # Test with default radius
        op = BlurOperation()
        assert op.radius == 2
        
        # Test with custom radius
        op = BlurOperation(radius=5)
        assert op.radius == 5
    
    def test_apply(self):
        """Test applying the blur operation."""
        # Create a test image
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Apply the operation with default radius
        op = BlurOperation()
        result = op.apply(img_pack)
        
        # Check the result
        assert result is not img_pack  # Should be a new instance
        assert result.pil_img is not img_pack.pil_img  # Should be a new image
        blur_context = result.get_context('blur')
        assert blur_context.blur_applied is True
        assert blur_context.blur_radius == 2
        
        # Apply the operation with custom radius
        op = BlurOperation(radius=3.5)
        result = op.apply(img_pack)
        
        # Check the result
        blur_context = result.get_context('blur')
        assert blur_context.blur_radius == 3.5
    
    def test_method_chaining(self):
        """Test that the operation can be called via method chaining."""
        # Create an image
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Call the operation via method chaining
        result = img_pack.blur(radius=1.5)
        
        # Check the result
        blur_context = result.get_context('blur')
        assert blur_context.blur_applied is True
        assert blur_context.blur_radius == 1.5
    
    def test_blur_effect(self, small_img_pack):
        """Test that the blur effect is actually applied to the image."""
        # Get the original image data
        original_data = small_img_pack.pil_img.tobytes()
        
        # Apply blur with a large radius to ensure visible effect
        result = small_img_pack.blur(radius=10)
        blurred_data = result.pil_img.tobytes()
        
        # The blurred image data should be different from the original
        assert blurred_data != original_data