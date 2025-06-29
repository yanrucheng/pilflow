#!/usr/bin/env python3
"""
Pilflow Context System Demo

This script demonstrates the new structured context system in Pilflow,
showing how operations can register context data classes and how they
interact with each other through typed context data.
"""

import json
from PIL import Image
from pilflow import ImgPack, Operation
from pilflow.core.context import ContextData
from pilflow.contexts.resolution_decision import ResolutionDecisionContextData
from jinnang.media.resolution import ResolutionPreset
from pilflow.contexts.resize import ResizeContextData
from pilflow.contexts.blur import BlurContextData


def create_sample_image(width: int = 1920, height: int = 1080) -> Image.Image:
    """Create a sample image for demonstration."""
    img = Image.new('RGB', (width, height), color='lightblue')
    return img


def demo_basic_context_usage():
    """Demonstrate basic context data creation and usage."""
    print("=== Basic Context Data Usage ===")
    
    # Create resolution decision context data
    resolution_data = ResolutionDecisionContextData(
        resolution_preset=ResolutionPreset.RES_1080P
    )
    
    print(f"Resolution preset: {resolution_data.resolution_preset}")
    print(f"Resolution preset value: {resolution_data.resolution_preset.value}")
    
    # JSON serialization
    json_str = resolution_data.to_json()
    print(f"JSON: {json_str}")
    
    # Restore from JSON
    restored = ResolutionDecisionContextData.from_json(json_str)
    print(f"Restored preset: {restored.resolution_preset}")
    print()


def demo_imgpack_integration():
    """Demonstrate ImgPack integration with structured contexts."""
    print("=== ImgPack Integration ===")
    
    # Create image and ImgPack
    img = create_sample_image(1920, 1080)
    img_pack = ImgPack(img)
    
    # Add resolution decision context
    resolution_context = ResolutionDecisionContextData(
        resolution_preset=ResolutionPreset.RES_1080P
    )
    img_pack.add_context(resolution_context)
    
    # Add resize context
    resize_context = ResizeContextData(
        current_width=1920,
        current_height=1080,
        target_width=1280,
        target_height=720,
        resized=False
    )
    img_pack.add_context(resize_context)
    
    # Check available contexts
    print(f"Available contexts: {list(img_pack.get_all_contexts().keys())}")
    print(f"Has resolution_decision context: {img_pack.has_context('resolution_decision')}")
    print(f"Has blur context: {img_pack.has_context('blur')}")
    
    # Get context data
    resolution = img_pack.get_context('resolution_decision')
    print(f"Resolution preset: {resolution.resolution_preset}")
    
    resize = img_pack.get_context('resize')
    print(f"Target dimensions: {resize.target_width}x{resize.target_height}")
    print(f"Has target dimensions: {resize.has_target_dimensions()}")
    print()


def demo_json_serialization():
    """Demonstrate JSON serialization of individual context data."""
    print("=== JSON Serialization ===")
    
    # Create and serialize individual context data
    resolution_data = ResolutionDecisionContextData(
        resolution_preset=ResolutionPreset.RES_720P
    )
    
    blur_data = BlurContextData(
        blur_applied=True,
        blur_radius=2.5
    )
    
    # Serialize individual contexts to JSON
    resolution_json = resolution_data.to_json()
    blur_json = blur_data.to_json()
    
    print("Serialized contexts:")
    print(f"  resolution_decision: {resolution_json}")
    print(f"  blur: {blur_json}")
    
    # Restore from JSON
    restored_resolution = ResolutionDecisionContextData.from_json(resolution_json)
    restored_blur = BlurContextData.from_json(blur_json)
    
    print(f"\nRestored resolution preset: {restored_resolution.resolution_preset}")
    print(f"Restored blur applied: {restored_blur.blur_applied}")
    print(f"Restored blur radius: {restored_blur.blur_radius}")
    print()


def demo_operation_pipeline():
    """Demonstrate operations using the new context system."""
    print("=== Operation Pipeline with Context System ===")
    
    # Create a large image
    img = create_sample_image(3840, 2160)  # 4K image
    img_pack = ImgPack(img)
    
    print(f"Original image size: {img.size}")
    
    # Apply resolution analysis
    result = img_pack.decide_resolution()
    resolution_context = result.get_context('resolution_decision')
    print(f"Resolution preset: {resolution_context.resolution_preset}")
    print(f"Resolution value: {resolution_context.resolution_preset.value}")
    
    # Apply resize operation
    result = result.resize(width=1920, height=1080)
    resize_context = result.get_context('resize')
    print(f"Resized to: {result.pil_img.size}")
    print(f"Scale factor: {resize_context.calculate_scale_factor():.2f}")
    
    # Apply blur
    result = result.blur(radius=1.5)
    blur_context = result.get_context('blur')
    print(f"Blur applied: {blur_context.blur_applied}")
    print(f"Blur intensity: {blur_context.get_blur_intensity()}")
    
    # Show all contexts
    print(f"\nFinal contexts: {list(result.get_all_contexts().keys())}")
    print()


def demo_missing_context_logging():
    """Demonstrate missing context logging functionality."""
    print("=== Missing Context Logging ===")
    
    img = create_sample_image()
    img_pack = ImgPack(img)
    
    # Check for missing contexts
    required_contexts = ['resolution_decision', 'resize', 'blur']
    missing = img_pack.get_missing_contexts(required_contexts)
    print(f"Missing contexts: {missing}")
    
    # Log missing contexts
    img_pack.log_missing_contexts(missing, 'demo_operation')
    
    # Add one context and check again
    img_pack.add_context(ResolutionDecisionContextData(
        resolution_preset=ResolutionPreset.RES_1080P
    ))
    
    missing_after = img_pack.get_missing_contexts(required_contexts)
    print(f"Missing contexts after adding resolution: {missing_after}")
    print()


def demo_custom_context_class():
    """Demonstrate creating a custom context data class."""
    print("=== Custom Context Data Class ===")
    
    class ColorAnalysisContextData(ContextData):
        """Context data for color analysis results."""
        
        def validate(self):
            """Validate color analysis data."""
            required_fields = ['dominant_color', 'color_count', 'brightness']
            for field in required_fields:
                if field not in self._data:
                    raise ValueError(f"{field} is required")
            
            if not isinstance(self._data['color_count'], int) or self._data['color_count'] < 0:
                raise ValueError("color_count must be a non-negative integer")
            
            if not 0 <= self._data['brightness'] <= 1:
                raise ValueError("brightness must be between 0 and 1")
        
        @property
        def dominant_color(self) -> tuple:
            """Get the dominant color as RGB tuple."""
            return tuple(self._data['dominant_color'])
        
        @property
        def color_count(self) -> int:
            """Get the number of unique colors."""
            return self._data['color_count']
        
        @property
        def brightness(self) -> float:
            """Get the image brightness (0-1)."""
            return self._data['brightness']
        
        def is_bright(self) -> bool:
            """Check if the image is considered bright."""
            return self.brightness > 0.7
        
        def is_colorful(self) -> bool:
            """Check if the image has many colors."""
            return self.color_count > 1000
    
    # Create and use the custom context
    color_context = ColorAnalysisContextData(
        dominant_color=[120, 150, 200],
        color_count=1500,
        brightness=0.8
    )
    
    print(f"Dominant color: {color_context.dominant_color}")
    print(f"Color count: {color_context.color_count}")
    print(f"Brightness: {color_context.brightness}")
    print(f"Is bright: {color_context.is_bright()}")
    print(f"Is colorful: {color_context.is_colorful()}")
    
    # Test JSON serialization
    json_str = color_context.to_json()
    print(f"JSON serialization: {json_str}")
    
    # Add to ImgPack
    img = create_sample_image()
    img_pack = ImgPack(img)
    img_pack.add_context(color_context)
    
    print(f"Context added to ImgPack: {img_pack.has_context('color_analysis')}")
    print(f"Context name inferred as: 'color_analysis'")
    print()


def main():
    """Run all demonstrations."""
    print("Pilflow Context System Demonstration")
    print("===================================\n")
    
    demo_basic_context_usage()
    demo_imgpack_integration()
    demo_json_serialization()
    demo_operation_pipeline()
    demo_missing_context_logging()
    demo_custom_context_class()
    
    print("Demo completed successfully!")


if __name__ == '__main__':
    main()