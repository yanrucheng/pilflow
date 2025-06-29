from PIL import Image
from pilflow import ImgPack
from pilflow.operations.decide_resolution import DecideResolutionOperation
from jinnang.media.resolution import ResolutionPreset


class TestDecideResolutionOperation:
    """Tests for the DecideResolutionOperation class."""
    
    def test_registration(self):
        """Test that the operation is registered with ImgPack."""
        assert 'decide_resolution' in ImgPack._operations
        assert ImgPack._operations['decide_resolution'] is DecideResolutionOperation
    
    def test_init(self):
        """Test initialization with different resolution presets."""
        # Test with 1080P preset
        op = DecideResolutionOperation(ResolutionPreset.RES_1080P)
        assert op.resolution_preset == ResolutionPreset.RES_1080P
        
        # Test with 720P preset
        op = DecideResolutionOperation(ResolutionPreset.RES_720P)
        assert op.resolution_preset == ResolutionPreset.RES_720P
    
    def test_apply_with_standard_preset(self):
        """Test applying the decide resolution operation with standard presets."""
        # Create a test image
        img = Image.new('RGB', (1920, 1080))
        img_pack = ImgPack(img)
        
        # Apply the operation with 720P preset
        op = DecideResolutionOperation(ResolutionPreset.RES_720P)
        result = op.apply(img_pack)
        
        # Check the result
        assert result is not img_pack  # Should be a new instance
        assert result.pil_img is img_pack.pil_img  # Image should not change
        
        # Check context data
        resolution_decision_context = result.get_context('resolution_decision')
        assert resolution_decision_context is not None
        assert resolution_decision_context.resolution_preset == ResolutionPreset.RES_720P
    
    def test_apply_with_original_preset(self):
        """Test applying the decide resolution operation with ORIGINAL preset."""
        # Create a test image
        img = Image.new('RGB', (800, 600))
        img_pack = ImgPack(img)
        
        # Apply the operation with ORIGINAL preset
        op = DecideResolutionOperation(ResolutionPreset.ORIGINAL)
        result = op.apply(img_pack)
        
        # Check the result
        assert result is not img_pack  # Should be a new instance
        assert result.pil_img is img_pack.pil_img  # Image should not change
        
        # Check context data - should store ORIGINAL preset
        resolution_decision_context = result.get_context('resolution_decision')
        assert resolution_decision_context is not None
        assert resolution_decision_context.resolution_preset == ResolutionPreset.ORIGINAL
    
    def test_method_chaining(self):
        """Test that the operation can be called via method chaining."""
        img = Image.new('RGB', (1920, 1080))
        img_pack = ImgPack(img)
        
        # Test chaining
        result = img_pack.decide_resolution(ResolutionPreset.RES_1080P)
        
        resolution_decision_context = result.get_context('resolution_decision')
        assert resolution_decision_context.resolution_preset == ResolutionPreset.RES_1080P
        assert isinstance(result.pil_img, Image.Image)
    
    def test_multiple_decisions(self):
        """Test multiple resolution decisions in sequence."""
        img = Image.new('RGB', (1920, 1080))
        img_pack = ImgPack(img)
        
        # First decision: 1080P
        result1 = img_pack.decide_resolution(ResolutionPreset.RES_1080P)
        context1 = result1.get_context('resolution_decision')
        assert context1.resolution_preset == ResolutionPreset.RES_1080P
        
        # Second decision: 720P (should override the first)
        result2 = result1.decide_resolution(ResolutionPreset.RES_720P)
        context2 = result2.get_context('resolution_decision')
        assert context2.resolution_preset == ResolutionPreset.RES_720P