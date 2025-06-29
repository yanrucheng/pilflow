import os
import tempfile
import shutil
import hashlib
import urllib.request
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TestDataManager:
    """Manages test image data for pilflow tests.
    
    This class handles downloading and caching test images in the /tmp directory
    to avoid interfering with the workspace.
    """
    
    # Default test images with their URLs (hash verification disabled for now)
    DEFAULT_TEST_IMAGES = {
        'small.jpg': {
            'url': 'https://raw.githubusercontent.com/python-pillow/Pillow/master/Tests/images/hopper.jpg',
            'md5': None,  # Disabled hash verification
            'size': (128, 128)
        },
        'large.jpg': {
            'url': 'https://raw.githubusercontent.com/python-pillow/Pillow/master/Tests/images/flower.jpg',
            'md5': None,  # Disabled hash verification
            'size': (640, 480)
        },
        'transparent.png': {
            'url': 'https://raw.githubusercontent.com/python-pillow/Pillow/master/Tests/images/transparent.png',
            'md5': None,  # Disabled hash verification
            'size': (200, 200)
        }
    }
    
    def __init__(self):
        """Initialize the test data manager."""
        # Create a unique directory in /tmp for test data
        self.data_dir = Path(tempfile.gettempdir()) / 'pilflow_test_data'
        self.data_dir.mkdir(exist_ok=True)
        logger.info(f"Test data directory: {self.data_dir}")
    
    def get_image_path(self, image_name):
        """Get the path to a test image, downloading it if necessary.
        
        Args:
            image_name: Name of the test image (e.g., 'small.jpg')
            
        Returns:
            Path: Path to the test image
        """
        if image_name not in self.DEFAULT_TEST_IMAGES:
            raise ValueError(f"Unknown test image: {image_name}")
        
        image_path = self.data_dir / image_name
        
        # If the image doesn't exist or has the wrong hash, download it
        if not image_path.exists() or not self._verify_hash(image_path, self.DEFAULT_TEST_IMAGES[image_name]['md5']):
            self._download_image(image_name)
        
        return image_path
    
    def _download_image(self, image_name):
        """Download a test image.
        
        Args:
            image_name: Name of the test image to download
        """
        image_info = self.DEFAULT_TEST_IMAGES[image_name]
        image_path = self.data_dir / image_name
        
        logger.info(f"Downloading test image: {image_name}")
        try:
            urllib.request.urlretrieve(image_info['url'], image_path)
            
            # Verify the downloaded image
            if not self._verify_hash(image_path, image_info['md5']):
                logger.warning(f"Downloaded image has incorrect hash: {image_name}")
                raise ValueError(f"Downloaded image has incorrect hash: {image_name}")
                
            logger.info(f"Successfully downloaded: {image_name}")
        except Exception as e:
            logger.error(f"Failed to download {image_name}: {e}")
            raise
    
    def _verify_hash(self, file_path, expected_md5):
        """Verify the MD5 hash of a file.
        
        Args:
            file_path: Path to the file to verify
            expected_md5: Expected MD5 hash (None to skip verification)
            
        Returns:
            bool: True if the hash matches or verification is skipped, False otherwise
        """
        if not file_path.exists():
            return False
            
        # Skip verification if expected_md5 is None
        if expected_md5 is None:
            return True
            
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
            return file_hash == expected_md5
    
    def cleanup(self):
        """Remove all downloaded test data."""
        if self.data_dir.exists():
            shutil.rmtree(self.data_dir)
            logger.info(f"Removed test data directory: {self.data_dir}")

# Singleton instance for easy access
data_manager = TestDataManager()

def get_test_image(image_name):
    """Get the path to a test image.
    
    Args:
        image_name: Name of the test image (e.g., 'small.jpg')
        
    Returns:
        Path: Path to the test image
    """
    return data_manager.get_image_path(image_name)

def cleanup_test_data():
    """Clean up all test data."""
    data_manager.cleanup()