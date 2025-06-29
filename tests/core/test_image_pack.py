import pytest
from pathlib import Path
from PIL import Image

import base64
import binascii
import pytest
from io import BytesIO
from pilflow import ImgPack
from pilflow.core.image_pack import ImgPack as CoreImgPack # To access static methods directly
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


class TestImgPackStaticMethods:
    """Tests for the static methods of ImgPack class."""

    def test_from_base64_valid(self, small_image):
        """Test from_base64 with a valid base64 string."""
        buffered = BytesIO()
        small_image.save(buffered, format="PNG")
        base64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')

        img_pack = CoreImgPack.from_base64(base64_string, test_context='value')
        assert isinstance(img_pack, CoreImgPack)
        assert isinstance(img_pack.pil_img, Image.Image)
        assert img_pack.context == {'test_context': 'value'}
        # Compare images by converting back to base64 or by pixel data
        buffered_result = BytesIO()
        img_pack.pil_img.save(buffered_result, format="PNG")
        assert base64.b64encode(buffered_result.getvalue()).decode('utf-8') == base64_string

    def test_from_base64_invalid_string(self):
        """Test from_base64 with an invalid base64 string."""
        with pytest.raises(ValueError, match="Invalid base64 string"):
            CoreImgPack.from_base64("not-a-valid-base64-string")

    def test_from_base64_not_image_data(self):
        """Test from_base64 with base64 data that is not an image."""
        # Base64 encoded string "hello world"
        not_image_base64 = base64.b64encode(b"hello world").decode('utf-8')
        with pytest.raises(Image.UnidentifiedImageError, match="Decoded data is not a valid image"):
            CoreImgPack.from_base64(not_image_base64)

    def test_from_file_valid(self, small_image_path):
        """Test from_file with a valid file path."""
        img_pack = CoreImgPack.from_file(small_image_path, test_context='value')
        assert isinstance(img_pack, CoreImgPack)
        assert isinstance(img_pack.pil_img, Image.Image)
        assert img_pack.context == {'test_context': 'value'}
        # Verify image content (e.g., mode and size)
        original_image = Image.open(small_image_path)
        assert img_pack.pil_img.mode == original_image.mode
        assert img_pack.pil_img.size == original_image.size

    def test_from_file_nonexistent(self):
        """Test from_file with a nonexistent file path."""
        with pytest.raises(FileNotFoundError, match="Image file not found"):
            CoreImgPack.from_file("nonexistent_file.jpg")

    def test_from_file_invalid_image_content(self, tmp_path):
        """Test from_file with a file that is not a valid image."""
        text_file = tmp_path / 'test.txt'
        text_file.write_text('This is not an image')
        with pytest.raises(Image.UnidentifiedImageError, match="File is not a valid image"):
            CoreImgPack.from_file(str(text_file))