#!/usr/bin/env python3
"""Minimal example demonstrating the decide_resolution operation.

This example shows how to use the DecideResolutionOperation to analyze
image resolution and make resolution decisions for further processing.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from PIL import Image
from pilflow.core.image_pack import ImgPack
from jinnang.media.resolution import ResolutionPreset


def create_sample_image(width=1920, height=1080):
    """Create a sample image for demonstration.
    
    Args:
        width: Image width
        height: Image height
        
    Returns:
        PIL.Image: Sample image
    """
    return Image.new('RGB', (width, height), color='lightblue')


def main():
    """Demonstrate decide_resolution operation."""
    print("Decide Resolution Operation - Minimal Example")
    print("============================================\n")
    
    # Test with different image sizes
    test_cases = [
        (640, 480, "SD (480p)"),
        (1280, 720, "HD (720p)"),
        (1920, 1080, "Full HD (1080p)"),
        (2560, 1440, "QHD (1440p)"),
        (3840, 2160, "4K (2160p)")
    ]
    
    for width, height, description in test_cases:
        print(f"Testing {description} - {width}x{height}:")
        
        # Create image and ImgPack
        img = create_sample_image(width, height)
        img_pack = ImgPack(img)
        
        # Apply decide_resolution operation
        result = img_pack.decide_resolution()
        
        # Get the resolution decision context
        resolution_context = result.get_context('resolution_decision')
        
        # Display results
        print(f"  Original size: {img.size}")
        print(f"  Decided preset: {resolution_context.resolution_preset}")
        print(f"  Preset value: {resolution_context.resolution_preset.value}")
        print(f"  Context available: {result.has_context('resolution_decision')}")
        print()
    
    # Demonstrate using the context for resize operation
    print("Using resolution decision for resize:")
    img = create_sample_image(3840, 2160)  # 4K image
    img_pack = ImgPack(img)
    
    # First decide resolution
    result = img_pack.decide_resolution()
    resolution_context = result.get_context('resolution_decision')
    print(f"4K image decided preset: {resolution_context.resolution_preset}")
    
    # Then resize using the decision (resize operation can use this context)
    resized_result = result.resize()  # Will use resolution_decision context
    print(f"Resized to: {resized_result.pil_img.size}")
    
    # Show available contexts
    contexts = list(resized_result.get_all_contexts().keys())
    print(f"Available contexts: {contexts}")
    
    print("\nExample completed successfully!")


if __name__ == '__main__':
    main()