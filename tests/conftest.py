import pytest
import os
import sys
from pathlib import Path
from PIL import Image

# Add the src directory to the path so we can import the package
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from pilflow import ImgPack
from tests.test_data.data_manager import get_test_image, cleanup_test_data

@pytest.fixture(scope="session")
def test_images():
    """Fixture that provides paths to test images.
    
    Returns:
        dict: Dictionary mapping image names to their file paths
    """
    images = {
        'small': get_test_image('small.jpg'),
        'large': get_test_image('large.jpg'),
        'transparent': get_test_image('transparent.png')
    }
    yield images
    # Clean up test data after all tests are done
    cleanup_test_data()

@pytest.fixture
def small_image_path(test_images):
    """Fixture that provides the path to a small test image."""
    return test_images['small']

@pytest.fixture
def large_image_path(test_images):
    """Fixture that provides the path to a large test image."""
    return test_images['large']

@pytest.fixture
def transparent_image_path(test_images):
    """Fixture that provides the path to a transparent test image."""
    return test_images['transparent']

@pytest.fixture
def small_image(small_image_path):
    """Fixture that provides a PIL Image object for a small test image."""
    return Image.open(small_image_path)

@pytest.fixture
def large_image(large_image_path):
    """Fixture that provides a PIL Image object for a large test image."""
    return Image.open(large_image_path)

@pytest.fixture
def transparent_image(transparent_image_path):
    """Fixture that provides a PIL Image object for a transparent test image."""
    return Image.open(transparent_image_path)

@pytest.fixture
def small_img_pack(small_image):
    """Fixture that provides an ImgPack object for a small test image."""
    return ImgPack(small_image)

@pytest.fixture
def large_img_pack(large_image):
    """Fixture that provides an ImgPack object for a large test image."""
    return ImgPack(large_image)

@pytest.fixture
def transparent_img_pack(transparent_image):
    """Fixture that provides an ImgPack object for a transparent test image."""
    return ImgPack(transparent_image)