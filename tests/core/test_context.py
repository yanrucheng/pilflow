import pytest
import json
from PIL import Image
from pilflow.core.context import ContextData
from pilflow.core.image_pack import ImgPack
from pilflow.contexts.resolution import ResolutionContextData
from pilflow.contexts.resize import ResizeContextData
from pilflow.contexts.blur import BlurContextData


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
    
    def test_json_serialization(self):
        """Test JSON serialization and deserialization."""
        @ContextData.register
        class SimpleContextData(ContextData):
            def validate(self):
                if 'value' not in self._data:
                    raise ValueError("value is required")
        
        # Create context data
        context = SimpleContextData(value=42, name="test")
        
        # Test to_dict
        data_dict = context.to_dict()
        assert data_dict == {'value': 42, 'name': 'test'}
        
        # Test to_json
        json_str = context.to_json()
        parsed = json.loads(json_str)
        assert parsed == {'value': 42, 'name': 'test'}
        
        # Test from_dict
        restored = SimpleContextData.from_dict(data_dict)
        assert restored == context
        
        # Test from_json
        restored_from_json = SimpleContextData.from_json(json_str)
        assert restored_from_json == context


class TestResolutionContextData:
    """Tests for ResolutionContextData."""
    
    def test_initialization(self):
        """Test resolution context data initialization."""
        context = ResolutionContextData(
            original_width=1920,
            original_height=1080,
            resolution_category="Full HD",
            aspect_ratio=16/9
        )
        
        assert context.original_width == 1920
        assert context.original_height == 1080
        assert context.resolution_category == "Full HD"
        assert abs(context.aspect_ratio - 16/9) < 0.01
    
    def test_validation(self):
        """Test resolution context data validation."""
        # Valid data should not raise
        ResolutionContextData(
            original_width=1920,
            original_height=1080,
            resolution_category="Full HD",
            aspect_ratio=1920/1080
        )
        
        # Invalid width
        with pytest.raises(ValueError, match="original_width must be a positive integer"):
            ResolutionContextData(
                original_width=-1,
                original_height=1080,
                resolution_category="Full HD",
                aspect_ratio=16/9
            )
        
        # Invalid category
        with pytest.raises(ValueError, match="resolution_category must be one of"):
            ResolutionContextData(
                original_width=1920,
                original_height=1080,
                resolution_category="Invalid",
                aspect_ratio=16/9
            )
        
        # Mismatched aspect ratio
        with pytest.raises(ValueError, match="aspect_ratio.*doesn't match dimensions"):
            ResolutionContextData(
                original_width=1920,
                original_height=1080,
                resolution_category="Full HD",
                aspect_ratio=1.0  # Wrong ratio
            )
    
    def test_properties(self):
        """Test resolution context data properties."""
        context = ResolutionContextData(
            original_width=3840,
            original_height=2160,
            resolution_category="4K",
            aspect_ratio=16/9
        )
        
        assert context.total_pixels == 3840 * 2160
        assert context.is_4k()
        assert context.is_hd_or_better()
        assert context.is_landscape()
        assert not context.is_portrait()
        assert not context.is_square()
    
    def test_registration(self):
        """Test that ResolutionContextData is properly registered."""
        registered_classes = ContextData.get_registered_classes()
        assert 'resolution' in registered_classes
        assert registered_classes['resolution'] is ResolutionContextData


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


class TestImgPackContextIntegration:
    """Tests for ImgPack integration with structured contexts."""
    
    def test_add_and_get_context(self):
        """Test adding and retrieving structured context data."""
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Add resolution context
        resolution_context = ResolutionContextData(
            original_width=100,
            original_height=100,
            resolution_category="SD",
            aspect_ratio=1.0
        )
        img_pack.add_context(resolution_context)
        
        # Test retrieval
        retrieved = img_pack.get_context('resolution')
        assert retrieved is resolution_context
        assert img_pack.has_context('resolution')
        
        # Test legacy context data is also updated
        assert img_pack.context['original_width'] == 100
        assert img_pack.context['resolution_category'] == "SD"
    
    def test_json_serialization(self):
        """Test ImgPack JSON serialization with structured contexts."""
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Add multiple contexts
        resolution_context = ResolutionContextData(
            original_width=100,
            original_height=100,
            resolution_category="SD",
            aspect_ratio=1.0
        )
        blur_context = BlurContextData(blur_applied=True, blur_radius=2)
        
        img_pack.add_context(resolution_context)
        img_pack.add_context(blur_context)
        
        # Test JSON serialization
        json_str = img_pack.to_json()
        data = json.loads(json_str)
        
        assert 'structured_contexts' in data
        assert 'resolution' in data['structured_contexts']
        assert 'blur' in data['structured_contexts']
        
        # Test deserialization
        restored_pack = ImgPack.from_json(json_str, img)
        assert restored_pack.has_context('resolution')
        assert restored_pack.has_context('blur')
        
        restored_resolution = restored_pack.get_context('resolution')
        assert restored_resolution.original_width == 100
        assert restored_resolution.resolution_category == "SD"
    
    def test_missing_context_logging(self, capsys):
        """Test missing context logging functionality."""
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Test missing contexts
        missing = img_pack.get_missing_contexts(['resolution', 'blur'])
        assert missing == ['resolution', 'blur']
        
        # Test logging
        img_pack.log_missing_contexts(['resolution'], 'test_operation')
        captured = capsys.readouterr()
        assert "Warning: test_operation requires missing contexts: ['resolution']" in captured.out
    
    def test_context_copy(self):
        """Test that structured contexts are properly copied."""
        img = Image.new('RGB', (100, 100))
        img_pack = ImgPack(img)
        
        # Add context
        resolution_context = ResolutionContextData(
            original_width=100,
            original_height=100,
            resolution_category="SD",
            aspect_ratio=1.0
        )
        img_pack.add_context(resolution_context)
        
        # Create copy
        copied_pack = img_pack.copy()
        
        # Verify context is copied
        assert copied_pack.has_context('resolution')
        copied_context = copied_pack.get_context('resolution')
        assert copied_context.original_width == 100
        
        # Verify they are separate instances (deep copy of context data)
        assert copied_context is not resolution_context
        
        # Verify modifying one doesn't affect the other
        copied_context._data['original_width'] = 200
        assert resolution_context.original_width == 100
        assert copied_context.original_width == 200