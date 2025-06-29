import pytest
from PIL import Image

from pilflow import ImgPack, from_file, Operation


class TestIntegration:
    """Integration tests for the pilflow package."""
    
    def test_operation_chaining(self, small_img_pack):
        """Test chaining multiple operations together."""
        # Chain operations
        result = (
            small_img_pack
            .decide_resolution()
            .resize(width=200)
            .blur(radius=1.5)
        )
        
        # Check the result
        assert result.pil_img.size[0] == 200  # Width should be 200
        assert 'resolution_category' in result.context
        assert 'blur_applied' in result.context
        assert result.context['blur_radius'] == 1.5
    
    def test_custom_operation(self, small_img_pack):
        """Test creating and using a custom operation."""
        # Create a custom operation
        class GrayscaleOperation(Operation):
            def apply(self, img_pack):
                grayscale_img = img_pack.pil_img.convert('L').convert('RGB')
                return img_pack.copy(new_img=grayscale_img, grayscale_applied=True)
        
        # Register the operation
        GrayscaleOperation.register('grayscale')
        
        # Use the custom operation
        result = small_img_pack.grayscale()
        
        # Check the result
        assert 'grayscale_applied' in result.context
        assert result.context['grayscale_applied'] is True
        
        # Check that the image is actually grayscale
        # In a grayscale image converted to RGB, all RGB values should be equal
        pixel = result.pil_img.getpixel((0, 0))
        if isinstance(pixel, tuple) and len(pixel) >= 3:
            assert pixel[0] == pixel[1] == pixel[2]
    
    def test_from_file_with_operations(self, small_image_path):
        """Test loading an image from file and applying operations."""
        # Load image and apply operations
        result = (
            from_file(small_image_path)
            .decide_resolution()
            .resize(width=150)
        )
        
        # Check the result
        assert result.pil_img.size[0] == 150
        assert 'resolution_category' in result.context
    
    def test_complex_pipeline(self, large_img_pack):
        """Test a more complex pipeline with multiple operations."""
        # Create a custom operation for this test
        class AddMetadataOperation(Operation):
            def __init__(self, **metadata):
                super().__init__(**metadata)
                self.metadata = metadata
                
            def apply(self, img_pack):
                return img_pack.copy(**self.metadata)
        
        # Register the operation
        AddMetadataOperation.register('add_metadata')
        
        # Create a complex pipeline
        result = (
            large_img_pack
            .decide_resolution()
            .resize(width=800)
            .blur(radius=2.5)
            .add_metadata(author='Test User', created_at='2023-01-01')
        )
        
        # Check the result
        assert result.pil_img.size[0] == 800
        assert 'resolution_category' in result.context
        assert 'blur_applied' in result.context
        assert result.context['blur_radius'] == 2.5
        assert result.context['author'] == 'Test User'
        assert result.context['created_at'] == '2023-01-01'