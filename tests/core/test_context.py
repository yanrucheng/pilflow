import pytest
import unittest
from PIL import Image
from pilflow.core.context import ContextData
from pilflow.core.image_pack import ImgPack
from pilflow.contexts.resize import ResizeContextData
from pilflow.contexts.blur import BlurContextData
from pilflow.contexts.resolution_decision import ResolutionDecisionContextData
from jinnang.media.resolution import ResolutionPreset


class TestContextData:
    """Tests for the ContextData base class."""
    
    def test_context_registration(self):
        """Test context data class registration."""
        @ContextData.register
        class TestContextData(ContextData):
            def validate(self):
                pass
        
        registered_classes = ContextData.get_registered_classes()
        assert 'test' in registered_classes
        assert registered_classes['test'] is TestContextData
    
    def test_context_registration_with_name(self):
        """Test context data class registration with explicit name."""
        @ContextData.register('custom_test')
        class CustomTestContextData(ContextData):
            def validate(self):
                pass
        
        registered_classes = ContextData.get_registered_classes()
        assert 'custom_test' in registered_classes
        assert registered_classes['custom_test'] is CustomTestContextData
    


class TestResizeContextData:
    """Tests for ResizeContextData."""
    
    def test_initialization(self):
        """Test resize context data initialization."""
        context = ResizeContextData(
            current_width=800,
            current_height=600,
            resized=True,
            resize_width=800,
            resize_height=600
        )
        
        assert context.current_width == 800
        assert context.current_height == 600
        assert context.resized is True
        assert context.resize_width == 800
        assert context.resize_height == 600
    
    def test_validation(self):
        """Test resize context data validation."""
        # Valid data should not raise
        ResizeContextData(
            current_width=800,
            current_height=600,
            resized=False
        )
        
        # Invalid when resized=True but no resize dimensions
        with pytest.raises(ValueError, match="resize_width and resize_height must be provided"):
            ResizeContextData(
                current_width=800,
                current_height=600,
                resized=True
            )
    
    def test_properties(self):
        """Test resize context data properties."""
        context = ResizeContextData(
            current_width=800,
            current_height=600,
            resized=True,
            target_width=1024,
            target_height=768,
            resize_width=800,
            resize_height=600
        )
        
        assert abs(context.current_aspect_ratio - 800/600) < 0.01
        assert abs(context.target_aspect_ratio - 1024/768) < 0.01
        assert abs(context.resize_aspect_ratio - 800/600) < 0.01
        assert context.has_target_dimensions()
        assert abs(context.calculate_scale_factor() - 1.0) < 0.01


class TestBlurContextData:
    """Tests for BlurContextData."""
    
    def test_initialization(self):
        """Test blur context data initialization."""
        context = BlurContextData(
            blur_applied=True,
            blur_radius=2.5
        )
        
        assert context.blur_applied is True
        assert context.blur_radius == 2.5
    
    def test_validation(self):
        """Test blur context data validation."""
        # Valid data should not raise
        BlurContextData(blur_applied=True, blur_radius=2)
        
        # Invalid when blur applied but radius is 0
        with pytest.raises(ValueError, match="blur_radius must be positive when blur_applied is True"):
            BlurContextData(blur_applied=True, blur_radius=0)
    
    def test_intensity_methods(self):
        """Test blur intensity classification methods."""
        light_blur = BlurContextData(blur_applied=True, blur_radius=1)
        assert light_blur.is_light_blur()
        assert light_blur.get_blur_intensity() == 'light'
        
        medium_blur = BlurContextData(blur_applied=True, blur_radius=3)
        assert medium_blur.is_medium_blur()
        assert medium_blur.get_blur_intensity() == 'medium'
        
        heavy_blur = BlurContextData(blur_applied=True, blur_radius=10)
        assert heavy_blur.is_heavy_blur()
        assert heavy_blur.get_blur_intensity() == 'heavy'
        
        no_blur = BlurContextData(blur_applied=False, blur_radius=0)
        assert no_blur.get_blur_intensity() == 'none'


class TestContextProducerRegistration(unittest.TestCase):
    """Test the new context producer registration system."""
    
    def test_producer_registration(self):
        """Test that operations are correctly registered as context producers."""
        # Check that DecideResolutionOperation is registered as a producer of resolution_decision context
        resolution_producers = ResolutionDecisionContextData.get_producer_operations('resolution_decision')
        self.assertIn('decide_resolution', resolution_producers)
        
        # Check that ResizeOperation is registered as a producer of resize context
        resize_producers = ResizeContextData.get_producer_operations('resize')
        self.assertIn('resize', resize_producers)
        
        # Check that BlurOperation is registered as a producer of blur context
        blur_producers = BlurContextData.get_producer_operations('blur')
        self.assertIn('blur', blur_producers)
    
    def test_get_all_producer_operations(self):
        """Test getting all producer operations."""
        all_producers = ContextData.get_all_producer_operations()
        
        # Check that we have producers for our context types
        self.assertIn('resolution_decision', all_producers)
        self.assertIn('resize', all_producers)
        self.assertIn('blur', all_producers)
        
        # Check specific producers
        self.assertIn('decide_resolution', all_producers['resolution_decision'])
        self.assertIn('resize', all_producers['resize'])
        self.assertIn('blur', all_producers['blur'])
    
    def test_missing_context_suggestions(self):
        """Test that missing context suggestions work with the new system."""
        import io
        import sys
        from unittest.mock import patch
        
        # Create an ImgPack
        test_image = Image.new('RGB', (100, 100), color='red')
        img_pack = ImgPack(test_image)
        
        # Capture stdout to check suggestions
        captured_output = io.StringIO()
        
        with patch('sys.stdout', captured_output):
            # Try to use resize operation without resolution_decision context
            # This should trigger missing context detection
            img_pack.log_missing_contexts(['resolution_decision'], 'resize')
        
        output = captured_output.getvalue()
        
        # Check that warning and suggestions are printed
        self.assertIn('Warning: resize requires missing contexts', output)
        self.assertIn('decide_resolution', output)
        self.assertIn('resolution_decision', output)


class TestImgPackContextIntegration:
    """Tests for ImgPack integration with structured contexts."""
    
    def test_add_and_get_context(self):
        """Test adding and retrieving structured context data."""
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Add resolution decision context
        resolution_context = ResolutionDecisionContextData(
            resolution_preset=ResolutionPreset.ORIGINAL
        )
        img_pack.add_context(resolution_context)
        
        # Test retrieval
        retrieved = img_pack.get_context('resolution_decision')
        assert retrieved is resolution_context
        assert img_pack.has_context('resolution_decision')
        
        # Test that context is properly stored
        assert retrieved.resolution_preset == ResolutionPreset.ORIGINAL
    
    def test_missing_context_logging(self, capsys):
        """Test missing context logging functionality."""
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Test missing contexts
        missing = img_pack.get_missing_contexts(['resolution_decision', 'blur'])
        assert missing == ['resolution_decision', 'blur']
        
        # Test logging
        img_pack.log_missing_contexts(['resolution_decision'], 'test_operation')
        captured = capsys.readouterr()
        assert "Warning: test_operation requires missing contexts: ['resolution_decision']" in captured.out
    
    def test_context_copy(self):
        """Test that structured contexts are properly copied."""
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Add context
        resolution_context = ResolutionDecisionContextData(
            resolution_preset=ResolutionPreset.RES_720P
        )
        img_pack.add_context(resolution_context)
        
        # Create copy
        copied_pack = img_pack.copy()
        
        # Verify context is copied
        assert copied_pack.has_context('resolution_decision')
        copied_context = copied_pack.get_context('resolution_decision')
        assert copied_context.resolution_preset == ResolutionPreset.RES_720P
        
        # Verify they are separate instances (deep copy of context data)
        assert copied_context is not resolution_context
        
        # Verify modifying one doesn't affect the other
        copied_context._data['resolution_preset'] = ResolutionPreset.RES_1080P
        assert resolution_context.resolution_preset == ResolutionPreset.RES_720P
        assert copied_context.resolution_preset == ResolutionPreset.RES_1080P