#!/usr/bin/env python3
"""
Example usage of pilflow pipeline with functional programming approach.

This demonstrates the new architecture where operations are separate classes
that register themselves with the ImgPack base class.
"""

from src.pilflow import from_file, Operation

# Example of creating a custom operation
@Operation.register('grayscale')
class GrayscaleOperation(Operation):
    """Custom operation to convert image to grayscale."""
    
    def apply(self, img_pack):
        """Convert the image to grayscale."""
        grayscale_img = img_pack.img.convert('L').convert('RGB')
        return img_pack.copy(new_img=grayscale_img, grayscale_applied=True)

def main():
    # Example usage of the pipeline
    try:
        # Create a pipeline - replace with actual image path
        pipeline = from_file('./test_image.jpg')
        
        if pipeline is not None:
            # Chain operations - all operations are dynamically available
            result = (pipeline
                     .decide_resolution()     # Add resolution info to context
                     .resize(width=800)       # Resize to specific width
                     .blur(radius=1.5)        # Apply blur with custom radius
                     .grayscale())            # Apply custom grayscale operation
            
            # Access the final image
            final_image = result.img
            
            # Access context data
            print("Context data:", result.context)
            print("Final image size:", final_image.size)
            
            # The beauty of this approach:
            # 1. ImgPack doesn't know about any specific operations
            # 2. Operations are completely independent
            # 3. Adding new operations requires no changes to base classes
            # 4. Operations can be defined anywhere and auto-register
            
    except Exception as e:
        print(f"Error in pipeline: {e}")

if __name__ == "__main__":
    main()