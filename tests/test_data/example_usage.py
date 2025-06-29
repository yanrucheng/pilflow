#!/usr/bin/env python3
"""
Example usage of the test data manager.

This script demonstrates how to use the test data manager to get test images.
"""

from pathlib import Path
from PIL import Image
import sys

# Add the parent directory to the path so we can import the test_data package
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.test_data.data_manager import get_test_image, cleanup_test_data

def main():
    # Get paths to test images
    small_image_path = get_test_image('small.jpg')
    large_image_path = get_test_image('large.jpg')
    transparent_image_path = get_test_image('transparent.png')
    
    print(f"Small image path: {small_image_path}")
    print(f"Large image path: {large_image_path}")
    print(f"Transparent image path: {transparent_image_path}")
    
    # Open the images to verify they exist
    small_image = Image.open(small_image_path)
    large_image = Image.open(large_image_path)
    transparent_image = Image.open(transparent_image_path)
    
    print(f"Small image size: {small_image.size}")
    print(f"Large image size: {large_image.size}")
    print(f"Transparent image size: {transparent_image.size}")
    
    # Clean up test data (optional - normally done by pytest fixture)
    if input("Clean up test data? (y/n): ").lower() == 'y':
        cleanup_test_data()
        print("Test data cleaned up.")

if __name__ == '__main__':
    main()