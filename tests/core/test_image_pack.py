import pytest
from pathlib import Path
from PIL import Image

from pilflow import ImgPack, from_file
from pilflow.core.operation import Operation


class TestImgPack:
    """Tests for the ImgPack class."""
    
    def test_init(self, small_image):
        """Test ImgPack initialization."""
        # Test with image only
        img_pack = ImgPack(small_image)
        assert img_pack.pil_img == small_image
        assert img_pack.context == {}
        
        # Test with image and context
        context = {'test': 'value'}
        img_pack = ImgPack(small_image, context_data=context)
        assert img_pack.pil_img == small_image
        assert img_pack.context == context
    
    def test_img_property(self, small_image):
        """Test the img property."""
        img_pack = ImgPack(small_image)
        assert img_pack.img is small_image
    
    def test_context_property(self, small_image):
        """Test the context property."""
        context = {'test': 'value'}
        img_pack = ImgPack(small_image, context_data=context)
        assert img_pack.context is img_pack._context_data
        assert img_pack.context == context
    
    def test_copy(self, small_image):
        """Test the copy method."""
        # Test with no changes
        img_pack = ImgPack(small_image, context_data={'original': True})
        copy = img_pack.copy()
        assert copy is not img_pack  # Should be a new instance
        assert copy.pil_img is img_pack.pil_img  # Should reference the same image
        assert copy.context is not img_pack.context  # Should be a new context dict
        assert copy.context == img_pack.context  # With the same content
        
        # Test with new image
        new_image = Image.new('RGB', (100, 100))
        copy = img_pack.copy(new_img=new_image)
        assert copy.pil_img is new_image
        assert copy.context == img_pack.context
        
        # Test with context updates
        copy = img_pack.copy(test_key='test_value')
        assert copy.context == {**img_pack.context, 'test_key': 'test_value'}
        
        # Test with both new image and context updates
        copy = img_pack.copy(new_img=new_image, test_key='test_value')
        assert copy.pil_img is new_image
        assert copy.context == {**img_pack.context, 'test_key': 'test_value'}
    
    def test_register_operation(self):
        """Test operation registration."""
        @Operation.register('test_op')
        class TestOperation(Operation):
            def apply(self, img_pack):
                return img_pack.copy(test_applied=True)
        
        # Test that the operation was registered
        img_pack = ImgPack(Image.new('RGB', (100, 100)))
        result = img_pack.test_op()
        assert result.context['test_applied'] is True
    
    def test_getattr_for_registered_operation(self, small_img_pack):
        """Test __getattr__ for registered operations."""
        @Operation.register('test_op')
        class TestOperation(Operation):
            def apply(self, img_pack):
                return img_pack.copy(test_applied=True)
        
        # Test that we can call the operation
        result = small_img_pack.test_op()
        assert result.context['test_applied'] is True
    
    def test_getattr_for_unregistered_operation(self, small_img_pack):
        """Test AttributeError for unregistered operations."""
        with pytest.raises(AttributeError):
            small_img_pack.nonexistent_operation()


class TestFromFile:
    """Tests for the from_file function."""
    
    def test_from_file_with_valid_file(self, small_image_path):
        """Test from_file with a valid file path."""
        img_pack = from_file(small_image_path)
        assert isinstance(img_pack, ImgPack)
        assert isinstance(img_pack.pil_img, Image.Image)
        assert img_pack.context == {}
    
    def test_from_file_with_invalid_file(self):
        """Test from_file with an invalid file path."""
        img_pack = from_file('nonexistent_file.jpg')
        assert img_pack is None
    
    def test_from_file_with_invalid_image(self, tmp_path):
        """Test from_file with a file that is not a valid image."""
        # Create a text file
        text_file = tmp_path / 'test.txt'
        text_file.write_text('This is not an image')
        
        img_pack = from_file(text_file)
        assert img_pack is None