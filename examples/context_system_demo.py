#!/usr/bin/env python3
"""
Pilflow Context System Demo

This script demonstrates the new structured context system in Pilflow,
showing how operations can register context data classes and how they
interact with each other through typed context data.
"""

from PIL import Image
from pilflow import ImgPack


def create_sample_image(width: int = 1920, height: int = 1080) -> Image.Image:
    """Create a sample image for demonstration."""
    img = Image.new('RGB', (width, height), color='lightblue')
    return img


def this_is_what_i_want_all_other_usage_of_context_should_be_removed():
    """Demonstrate operations using the new context system."""
    print("=== Operation Pipeline with Context System ===")
    
    # Create a large image
    img = create_sample_image(3840, 2160)  # 4K image
    img_pack = ImgPack(img)
    
    print(f"Original image size: {img.size}")
    
    # Successful pipeline: context is provided
    print("\n1. Successful pipeline with context:")
    pipeline = (img_pack
              .decide_resolution()  # this line adds context
              .resize() # this line reads context
    )
    
    print(f"Resized image size: {pipeline.pil_img.size}")
    print(f"Available contexts: {list(pipeline.get_all_contexts().keys())}")
    
    # Failed pipeline: context is missing
    print("\n2. Failed pipeline without context:")
    try:
        pipeline = (img_pack
                  .resize() # this line reads context. context missing this should raise error
        )
        print("ERROR: This should not succeed!")
    except ValueError as e:
        print(f"✓ Expected error caught: {e}")
    
    print("\nDemo completed successfully!")


def main():
    """Run the context system demonstration."""
    print("Pilflow Context System Demonstration")
    print("===================================\n")
    
    this_is_what_i_want_all_other_usage_of_context_should_be_removed()
    
    print("\nDemo completed successfully!")


if __name__ == '__main__':
    main()
