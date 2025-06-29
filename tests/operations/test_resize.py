import pytest
from PIL import Image

from pilflow import ImgPack
from pilflow.operations.resize import ResizeOperation
from pilflow.contexts.resolution_decision import ResolutionDecisionContextData
from jinnang.media.resolution import ResolutionPreset


class TestResizeOperation:
    """Tests for the ResizeOperation class."""
    
    def test_registration(self):
        """Test that the operation is registered with ImgPack."""
        assert 'resize' in ImgPack._operations
        assert ImgPack._operations['resize'] is ResizeOperation
    
    def test_init(self):
        """Test initialization with different parameters."""
        # Test with no parameters
        op = ResizeOperation()
        assert op.width is None
        assert op.height is None
        
        # Test with width only
        op = ResizeOperation(width=800)
        assert op.width == 800
        assert op.height is None
        
        # Test with height only
        op = ResizeOperation(height=600)
        assert op.width is None
        assert op.height == 600
        
        # Test with both width and height
        op = ResizeOperation(width=800, height=600)
        assert op.width == 800
        assert op.height == 600
        
        # Test with resolution preset
        op = ResizeOperation(resolution_preset=ResolutionPreset.RES_720P)
        assert op.resolution_preset == ResolutionPreset.RES_720P
        assert op.width is None
        assert op.height is None
    
    def test_apply_with_explicit_dimensions(self):
        """Test resizing with explicitly provided dimensions."""
        # Create a test image
        img = Image.new('RGB', (1000, 750))
        img_pack = ImgPack(img)
        
        # Test resizing with width only
        op = ResizeOperation(width=500)
        result = op.apply(img_pack)
        assert result.pil_img.size == (500, 375)  # Height should be proportional
        
        # Test resizing with height only
        op = ResizeOperation(height=300)
        result = op.apply(img_pack)
        assert result.pil_img.size == (400, 300)  # Width should be proportional
        
        # Test resizing with both width and height
        op = ResizeOperation(width=400, height=200)
        result = op.apply(img_pack)
        assert result.pil_img.size == (400, 200)  # Should match exactly
    
    def test_apply_with_resolution_decision_context(self):
        """Test resizing using ResolutionDecision context."""
        # Create a test image
        img = Image.new('RGB', (1000, 750))
        img_pack = ImgPack(img)
        
        # Add ResolutionDecision context
        resolution_context = ResolutionDecisionContextData(resolution_preset=ResolutionPreset.RES_720P)
        img_pack.add_context(resolution_context)
        
        # Apply the operation with no explicit dimensions
        op = ResizeOperation()
        result = op.apply(img_pack)
        
        # Check that the image was resized according to resolution preset
        assert result.pil_img.size == (1280, 720)
    
    def test_apply_fails_without_context_or_dimensions(self):
        """Test that operation fails when no ResolutionDecision context or explicit dimensions are provided."""
        # Create a test image
        img = Image.new('RGB', (1920, 1080))
        img_pack = ImgPack(img)
        
        # Apply the operation with no explicit dimensions and no ResolutionDecision context
        op = ResizeOperation()
        
        # Should raise ValueError with helpful message
        with pytest.raises(ValueError, match="ResizeOperation requires explicit dimensions or a ResolutionDecision context"):
            op.apply(img_pack)
    
    def test_apply_with_original_preset_context(self):
        """Test resizing with ORIGINAL preset in ResolutionDecision context."""
        # Create a test image
        img = Image.new('RGB', (640, 480))
        img_pack = ImgPack(img)
        
        # Add ResolutionDecision context with ORIGINAL preset
        resolution_context = ResolutionDecisionContextData(resolution_preset=ResolutionPreset.ORIGINAL)
        img_pack.add_context(resolution_context)
        
        # Apply the operation with no explicit dimensions
        op = ResizeOperation()
        result = op.apply(img_pack)
        
        # Check that the image was not resized (kept original size)
        assert result.pil_img.size == (640, 480)
    
    def test_method_chaining(self):
        """Test that the operation can be called via method chaining."""
        # Create an image
        img = Image.new('RGB', (1000, 750))
        img_pack = ImgPack(img)
        
        # Call the operation via method chaining
        result = img_pack.resize(width=500)
        
        # Check the result
        assert result.pil_img.size == (500, 375)
    
    def test_apply_with_resolution_preset(self):
        """Test resizing with ResolutionPreset parameter."""
        # Create a test image
        img = Image.new('RGB', (1920, 1080))
        img_pack = ImgPack(img)
        
        # Test resizing with 720P preset
        op = ResizeOperation(resolution_preset=ResolutionPreset.RES_720P)
        result = op.apply(img_pack)
        assert result.pil_img.size == (1280, 720)
        
        # Test resizing with ORIGINAL preset
        op = ResizeOperation(resolution_preset=ResolutionPreset.ORIGINAL)
        result = op.apply(img_pack)
        assert result.pil_img.size == (1920, 1080)  # Should keep original size
        
        # Test resizing with 4K preset
        op = ResizeOperation(resolution_preset=ResolutionPreset.RES_4K)
        result = op.apply(img_pack)
        assert result.pil_img.size == (3840, 2160)