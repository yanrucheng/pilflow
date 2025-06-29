#!/usr/bin/env python3
"""
Demo script showing the new context producer registration system in Pilflow.

This script demonstrates:
1. How operations register as producers of context data
2. How the system suggests operations when context is missing
3. The new decorator-based registration approach
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image
from pilflow import ImgPack
from pilflow.core.context import ContextData
from pilflow.contexts.resolution_decision import ResolutionDecisionContextData
from pilflow.contexts.resize import ResizeContextData
from pilflow.contexts.blur import BlurContextData

def main():
    print("=== Pilflow Context Producer Registration Demo ===")
    print()
    
    # 1. Show registered producer operations
    print("1. Registered Producer Operations:")
    all_producers = ContextData.get_all_producer_operations()
    
    for context_name, producers in all_producers.items():
        print(f"   {context_name} context can be produced by: {', '.join(producers)}")
    print()
    
    # 2. Show specific context producers
    print("2. Specific Context Producers:")
    resolution_producers = ResolutionDecisionContextData.get_producer_operations('resolution_decision')
    print(f"   Resolution decision context producers: {resolution_producers}")
    
    resize_producers = ResizeContextData.get_producer_operations('resize')
    print(f"   Resize context producers: {resize_producers}")
    
    blur_producers = BlurContextData.get_producer_operations('blur')
    print(f"   Blur context producers: {blur_producers}")
    print()
    
    # 3. Demonstrate missing context detection and suggestions
    print("3. Missing Context Detection and Suggestions:")
    
    # Create a test image
    test_image = Image.new('RGB', (800, 600), color='red')
    img_pack = ImgPack(test_image)
    
    print("   Creating ImgPack without any context data...")
    print("   Attempting to use resize operation (which may require resolution_decision context):")
    print()
    
    # This will trigger missing context detection
    try:
        # The resize operation will check for resolution context and suggest the producer
        resized = img_pack.resize(400, 300)
        print("   Resize completed successfully!")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # 4. Show the correct workflow
    print("4. Correct Workflow - Using Producer Operations:")
    print("   Step 1: Run decide_resolution to generate resolution_decision context")
    img_pack_with_resolution = img_pack.decide_resolution()
    
    print("   Step 2: Now resize operation can access resolution_decision context")
    resized = img_pack_with_resolution.resize(400, 300)
    
    print("   Step 3: Apply blur operation")
    blurred = resized.blur(radius=2.0)
    
    print("   All operations completed successfully!")
    print()
    
    # 5. Show context data in the final result
    print("5. Final Context Data:")
    final_contexts = blurred.get_all_contexts()
    for context_name, context_data in final_contexts.items():
        print(f"   {context_name}: {context_data}")
    print()
    
    # 6. Demonstrate custom operation registration
    print("6. Custom Operation Registration Example:")
    print("   You can create custom operations that register as context producers:")
    print()
    print("   @ResolutionDecisionContextData.register_as_producer")
    print("   @Operation.register")
    print("   class AutoResolutionDeciderOperation(Operation):")
    print("       def apply(self, img_pack):")
    print("           # Custom resolution logic")
    print("           return img_pack")
    print()
    print("   This would register 'auto_resolution_decider' as another producer")
    print("   of resolution_decision context data.")
    print()
    
    print("=== Demo Complete ===")

if __name__ == "__main__":
    main()