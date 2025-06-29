from pilflow.core.image_pack import ImgPack

def demo_imgpack_creation_at_a_glance():
    print("\n--- Basic Demo: ImgPack.from_file and ImgPack.from_base64 ---")

    # 1. Demonstrate ImgPack.from_file
    #    Assumes 'path/to/your/image.jpg' exists and is a valid image file.
    print("\n1. Creating ImgPack from a file:")
    # For demonstration, assume 'path/to/your/image.jpg' is a JPEG file.
    img_pack_from_file = ImgPack.from_file("path/to/your/image.jpg")
    print("   ImgPack.from_file(\"path/to/your/image.jpg\") called.")
    print(f"   Inferred format: {{img_pack_from_file.image_format}}")
    # In a real scenario, you would then use img_pack_from_file
    # print(f"   Image size: {img_pack_from_file.pil_img.size}") # Example usage
    # print(f"   Base64 output (should be JPEG): {img_pack_from_file.base64[:50]}...") # Example usage

    # 2. Demonstrate ImgPack.from_base64
    #    Assumes 'SGVsbG8gV29ybGQ=' is a valid base64 encoded image string.
    print("\n2. Creating ImgPack from a base64 string:")
    # This is a placeholder base64 string with a data URI prefix.
    # A real one would be much longer and contain actual image data.
    base64_placeholder_with_prefix = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wDAQEBAQEBAQEBAQ"
    img_pack_from_base64 = ImgPack.from_base64(base64_placeholder_with_prefix)
    print("   ImgPack.from_base64(\"data:image/jpeg;base64,...\") called.")
    print(f"   Inferred format: {{img_pack_from_base64.image_format}}")
    # In a real scenario, you would then use img_pack_from_base64
    # print(f"   Image size: {img_pack_from_base64.pil_img.size}") # Example usage
    # print(f"   Base64 output (should be JPEG): {img_pack_from_base64.base64[:50]}...") # Example usage

    print("\n--- Demo complete (for human understanding) ---")

if __name__ == '__main__':
    demo_imgpack_creation_at_a_glance()