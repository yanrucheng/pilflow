import pytest
from unittest.mock import MagicMock

from pilflow.core.operation import Consumer


class TestConsumer:
    """Tests for the Consumer base class."""

    def test_init(self):
        """Test Consumer initialization."""
        # Create a concrete subclass for testing
        class ConcreteConsumer(Consumer):
            def apply(self, img_pack):
                pass

        # Test with no args or kwargs
        op = ConcreteConsumer()
        assert op.args == ()
        assert op.kwargs == {}

        # Test with args
        op = ConcreteConsumer(1, 2, 3)
        assert op.args == (1, 2, 3)
        assert op.kwargs == {}

        # Test with kwargs
        op = ConcreteConsumer(a=1, b=2)
        assert op.args == ()
        assert op.kwargs == {'a': 1, 'b': 2}

        # Test with both args and kwargs
        op = ConcreteConsumer(1, 2, a=3, b=4)
        assert op.args == (1, 2)
        assert op.kwargs == {'a': 3, 'b': 4}

    def test_call(self):
        """Test the __call__ method."""
        # Create a mock for the apply method
        mock_apply = MagicMock(return_value=None)

        # Create a concrete subclass with the mock apply method
        class ConcreteConsumer(Consumer):
            apply = mock_apply

        # Create an instance and call it
        op = ConcreteConsumer()
        img_pack = MagicMock()
        result = op(img_pack)

        # Check that apply was called with the correct arguments
        mock_apply.assert_called_once_with(img_pack)
        assert result is None

    def test_abstract_apply_method(self):
        """Test that the apply method is abstract and must be implemented."""
        # Attempt to instantiate the abstract base class
        with pytest.raises(TypeError):
            Consumer()

        # Attempt to instantiate a subclass without implementing apply
        class IncompleteConsumer(Consumer):
            pass

        with pytest.raises(TypeError):
            IncompleteConsumer()