import pytest
from PIL import Image

from pilflow import ImgPack
from pilflow.operations.resolution import DecideResolutionOperation


class TestDecideResolutionOperation:
    """Tests for the DecideResolutionOperation class."""
    
    def test_registration(self):
        """Test that the operation is registered with ImgPack."""
        assert 'decide_resolution' in ImgPack._operations
        assert ImgPack._operations['decide_resolution'] is DecideResolutionOperation
    
    def test_apply_4k_image(self):
        """Test applying the operation to a 4K image."""
        # Create a 4K image
        img = Image.new('RGB', (3840, 2160))
        img_pack = ImgPack(img)
        
        # Apply the operation
        op = DecideResolutionOperation()
        result = op.apply(img_pack)
        
        # Check the result
        assert result is not img_pack  # Should be a new instance
        assert result.pil_img is img_pack.pil_img  # Should reference the same image
        assert result.context != {}  # Should have context data
        assert result.context['original_width'] == 3840
        assert result.context['original_height'] == 2160
        assert result.context['resolution_category'] == '4K'
        assert result.context['aspect_ratio'] == 3840 / 2160
    
    def test_apply_full_hd_image(self):
        """Test applying the operation to a Full HD image."""
        # Create a Full HD image
        img = Image.new('RGB', (1920, 1080))
        img_pack = ImgPack(img)
        
        # Apply the operation
        op = DecideResolutionOperation()
        result = op.apply(img_pack)
        
        # Check the result
        assert result.context['original_width'] == 1920
        assert result.context['original_height'] == 1080
        assert result.context['resolution_category'] == 'Full HD'
        assert result.context['aspect_ratio'] == 1920 / 1080
    
    def test_apply_hd_image(self):
        """Test applying the operation to an HD image."""
        # Create an HD image
        img = Image.new('RGB', (1280, 720))
        img_pack = ImgPack(img)
        
        # Apply the operation
        op = DecideResolutionOperation()
        result = op.apply(img_pack)
        
        # Check the result
        assert result.context['original_width'] == 1280
        assert result.context['original_height'] == 720
        assert result.context['resolution_category'] == 'HD'
        assert result.context['aspect_ratio'] == 1280 / 720
    
    def test_apply_sd_image(self):
        """Test applying the operation to an SD image."""
        # Create an SD image
        img = Image.new('RGB', (640, 480))
        img_pack = ImgPack(img)
        
        # Apply the operation
        op = DecideResolutionOperation()
        result = op.apply(img_pack)
        
        # Check the result
        assert result.context['original_width'] == 640
        assert result.context['original_height'] == 480
        assert result.context['resolution_category'] == 'SD'
        assert result.context['aspect_ratio'] == 640 / 480
    
    def test_method_chaining(self):
        """Test that the operation can be called via method chaining."""
        # Create an image
        img = Image.new('RGB', (1920, 1080))
        img_pack = ImgPack(img)
        
        # Call the operation via method chaining
        result = img_pack.decide_resolution()
        
        # Check the result
        assert result.context['resolution_category'] == 'Full HD'