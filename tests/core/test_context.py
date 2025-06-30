import unittest
from pilflow.core.context import ContextData
from pilflow.contexts.resize import ResizeContextData
from pilflow.contexts.blur import BlurContextData
from pilflow.contexts.resolution_decision import ResolutionDecisionContextData


class TestContextData(unittest.TestCase):
    """Tests for the ContextData base class."""

    def test_context_name_generation(self):
        """Test context name generation from class name."""
        class TestContextData(ContextData):
            pass

        # Test that context name is generated correctly
        self.assertEqual(TestContextData._get_context_name(), 'test')

    def test_context_name_generation_with_suffix(self):
        """Test context name generation with ContextData suffix."""
        class CustomTestContextData(ContextData):
            pass

        # Test that ContextData suffix is removed
        self.assertEqual(CustomTestContextData._get_context_name(), 'custom_test')


class TestContextProducerRegistration(unittest.TestCase):
    """Test the new context producer registration system."""

    def test_producer_registration(self):
        """Test that operations are correctly registered as context producers."""
        # Check that DecideResolutionOperation is registered as a producer of resolution_decision context
        resolution_producers = ResolutionDecisionContextData.get_producer_operations('resolution_decision')
        self.assertIn('decide_resolution', resolution_producers)

        # Check that ResizeOperation is registered as a producer of resize context
        resize_producers = ResizeContextData.get_producer_operations('resize')
        self.assertIn('resize', resize_producers)

        # Check that BlurOperation is registered as a producer of blur context
        blur_producers = BlurContextData.get_producer_operations('blur')
        self.assertIn('blur', blur_producers)

    def test_get_all_producer_operations(self):
        """Test getting all producer operations."""
        all_producers = ContextData.get_all_producer_operations()

        # Check that we have producers for our context types
        self.assertIn('resolution_decision', all_producers)
        self.assertIn('resize', all_producers)
        self.assertIn('blur', all_producers)

        # Check specific producers
        self.assertIn('decide_resolution', all_producers['resolution_decision'])
        self.assertIn('resize', all_producers['resize'])
        self.assertIn('blur', all_producers['blur'])