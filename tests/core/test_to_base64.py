import pytest
import base64
import re
from io import BytesIO
from PIL import Image
from pilflow import ImgPack
from pilflow.core.image_pack import ImgPack as CoreImgPack


class TestImgPackBase64:
    """Tests for the ImgPack base64 property."""
    
    def test_base64_property_default_format(self, small_image):
        """Test ImgPack base64 property with default format."""
        img_pack = ImgPack(small_image)
        
        result = img_pack.base64
        
        # Verify result is a string
        assert isinstance(result, str)
        
        # Verify it has the correct data URI format
        assert result.startswith("data:image/png;base64,")
        
        # Extract base64 data
        base64_data = result.split(',')[1]
        
        # Verify it's valid base64
        try:
            decoded = base64.b64decode(base64_data)
            assert len(decoded) > 0
        except Exception as e:
            pytest.fail(f"Result is not valid base64: {e}")
        
        # Verify we can recreate the image from the base64
        decoded_img = Image.open(BytesIO(base64.b64decode(base64_data)))
        assert decoded_img.size == small_image.size
    
    def test_base64_with_image_format(self, small_image):
        """Test ImgPack base64 property with specified image format."""
        img_pack = ImgPack(small_image, image_format="JPEG")
        
        result = img_pack.base64
        
        # Verify it has the correct data URI format for JPEG
        assert result.startswith("data:image/jpeg;base64,")
        
        # Extract and verify base64 data
        base64_data = result.split(',')[1]
        decoded = base64.b64decode(base64_data)
        decoded_img = Image.open(BytesIO(decoded))
        assert decoded_img.size == small_image.size
    
    def test_base64_different_formats(self, small_image):
        """Test ImgPack base64 property with different image formats."""
        formats = ["PNG", "JPEG"]
        results = {}
        
        for fmt in formats:
            img_pack = ImgPack(small_image, image_format=fmt)
            result = img_pack.base64
            results[fmt] = result
            
            # Verify each result is valid base64
            assert isinstance(result, str)
            assert result.startswith(f"data:image/{fmt.lower()};base64,")
            base64_data = result.split(',')[1]
            decoded = base64.b64decode(base64_data)
            decoded_img = Image.open(BytesIO(decoded))
            assert decoded_img.size == small_image.size
        
        # Results should be different for different formats
        assert results["PNG"] != results["JPEG"]


class TestToBase64TypePreservation:
    """Tests for type preservation in to_base64 operations."""
    
    def test_imgpack_base64_property_type(self, small_image):
        """Test that ImgPack.base64 property returns string type."""
        img_pack = ImgPack(small_image)
        
        result = img_pack.base64
        
        # Verify type is preserved
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Verify it's valid base64 with data URI format
        assert result.startswith("data:image/")
        base64_data = result.split(',')[1]
        decoded = base64.b64decode(base64_data)
        assert len(decoded) > 0
    
    def test_type_preservation_after_pipeline_operations(self, small_image):
        """Test that type is preserved after various pipeline operations."""
        # Create ImgPack with context data
        original_context = {'test_key': 'test_value', 'number': 42}
        img_pack = ImgPack(small_image, context_data=original_context)
        
        # Test base64 property type before any operations
        base64_before = img_pack.base64
        assert isinstance(base64_before, str)
        
        # Perform a copy operation (common pipeline operation)
        copied_pack = img_pack.copy()
        base64_after_copy = copied_pack.base64
        assert isinstance(base64_after_copy, str)
        
        # Verify the base64 strings are identical (same image)
        assert base64_before == base64_after_copy
        
        # Test with context modifications
        copied_pack_with_new_context = img_pack.copy(new_context={'modified': True})
        base64_after_context_change = copied_pack_with_new_context.base64
        assert isinstance(base64_after_context_change, str)
        
        # Base64 should still be the same (image unchanged)
        assert base64_before == base64_after_context_change
    
    def test_type_preservation_with_format_changes(self, small_image):
        """Test type preservation when changing image formats."""
        # Test with different image formats stored in ImgPack
        formats = ["PNG", "JPEG", None]  # None should default to PNG
        
        for fmt in formats:
            img_pack = ImgPack(small_image, image_format=fmt)
            base64_result = img_pack.base64
            
            # Type should always be string regardless of format
            assert isinstance(base64_result, str)
            assert len(base64_result) > 0
            
            # Should have data URI format
            assert base64_result.startswith("data:image/")
            
            # Should be valid base64 (extract the base64 part)
            base64_data = base64_result.split(',')[1]
            decoded = base64.b64decode(base64_data)
            assert len(decoded) > 0
    
    def test_roundtrip_type_preservation(self, small_image):
        """Test type preservation in roundtrip: image -> base64 -> image -> base64."""
        # Start with ImgPack
        original_pack = ImgPack(small_image, context_data={'original': True})
        
        # Convert to base64
        base64_str = original_pack.base64
        assert isinstance(base64_str, str)
        
        # Create new ImgPack from base64
        roundtrip_pack = CoreImgPack.from_base64(base64_str, roundtrip=True)
        
        # Convert back to base64
        roundtrip_base64 = roundtrip_pack.base64
        assert isinstance(roundtrip_base64, str)
        
        # Both base64 strings should be identical
        assert base64_str == roundtrip_base64
    
    def test_base64_property_different_formats_type_preservation(self, small_image):
        """Test type preservation when using base64 property with different formats."""
        # Test with different formats
        formats = ["PNG", "JPEG", "WEBP"]
        
        for fmt in formats:
            try:
                img_pack = ImgPack(small_image, context_data={'direct_test': True}, image_format=fmt)
                result = img_pack.base64
                
                # Type should always be string
                assert isinstance(result, str)
                assert len(result) > 0
                
                # Should have correct data URI format
                assert result.startswith(f"data:image/{fmt.lower()};base64,")
                
                # Should be valid base64
                base64_data = result.split(',')[1]
                decoded = base64.b64decode(base64_data)
                assert len(decoded) > 0
                
                # Should be able to recreate image
                recreated_img = Image.open(BytesIO(decoded))
                assert recreated_img.size == small_image.size
                
            except Exception as e:
                # Some formats might not be supported, that's okay
                if "cannot write mode" not in str(e).lower():
                    raise
    
    def test_type_consistency_across_multiple_calls(self, small_image):
        """Test that type remains consistent across multiple to_base64 calls."""
        img_pack = ImgPack(small_image)
        
        # Call base64 property multiple times
        results = []
        for i in range(5):
            result = img_pack.base64
            results.append(result)
            
            # Each result should be string type
            assert isinstance(result, str)
            assert len(result) > 0
        
        # All results should be identical (deterministic)
        for result in results[1:]:
            assert result == results[0]
            assert type(result) == type(results[0])