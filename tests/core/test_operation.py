import pytest
from unittest.mock import MagicMock
from PIL import Image

from pilflow import ImgPack, Operation


class TestOperation:
    """Tests for the Operation base class."""
    
    def test_init(self):
        """Test Operation initialization."""
        # Create a concrete subclass for testing
        class ConcreteOperation(Operation):
            def apply(self, img_pack):
                return img_pack
        
        # Test with no args or kwargs
        op = ConcreteOperation()
        assert op.args == ()
        assert op.kwargs == {}
        
        # Test with args
        op = ConcreteOperation(1, 2, 3)
        assert op.args == (1, 2, 3)
        assert op.kwargs == {}
        
        # Test with kwargs
        op = ConcreteOperation(a=1, b=2)
        assert op.args == ()
        assert op.kwargs == {'a': 1, 'b': 2}
        
        # Test with both args and kwargs
        op = ConcreteOperation(1, 2, a=3, b=4)
        assert op.args == (1, 2)
        assert op.kwargs == {'a': 3, 'b': 4}
    
    def test_call(self):
        """Test the __call__ method."""
        # Create a mock for the apply method
        mock_apply = MagicMock(return_value='result')
        
        # Create a concrete subclass with the mock apply method
        class ConcreteOperation(Operation):
            apply = mock_apply
        
        # Create an instance and call it
        op = ConcreteOperation()
        img_pack = MagicMock()
        result = op(img_pack)
        
        # Check that apply was called with the correct arguments
        mock_apply.assert_called_once_with(img_pack)
        assert result == 'result'
    
    def test_register(self):
        """Test the register class method."""
        # Create a concrete subclass
        class TestRegisterOperation(Operation):
            def apply(self, img_pack):
                return img_pack
        
        # Register the operation with a custom name using manual registration
        decorator_func = TestRegisterOperation.register('custom_name')
        registered_class = decorator_func(TestRegisterOperation)
        assert registered_class is TestRegisterOperation
        assert 'custom_name' in ImgPack._operations
        assert ImgPack._operations['custom_name'] is TestRegisterOperation
        
        # Register the operation with the default name
        class AnotherOperation(Operation):
            def apply(self, img_pack):
                return img_pack
        
        decorator_func2 = AnotherOperation.register()
        registered_class2 = decorator_func2(AnotherOperation)
        assert registered_class2 is AnotherOperation
        assert 'another' in ImgPack._operations
        assert ImgPack._operations['another'] is AnotherOperation
    
    def test_register_decorator(self):
        """Test operation registration using decorator syntax."""
        @Operation.register('decorator_test')
        class DecoratorTestOperation(Operation):
            def apply(self, img_pack):
                return img_pack.copy(test_applied=True)
        
        # Test that the operation was registered
        img_pack = ImgPack(Image.new('RGB', (100, 100)))
        result = img_pack.decorator_test()
        assert result.context['test_applied'] is True
    
    def test_register_decorator_auto_name(self):
        """Test operation registration using decorator with automatic name inference."""
        @Operation.register
        class TestAutoNameOperation(Operation):
            def apply(self, img_pack):
                return img_pack.copy(auto_name_applied=True)
        
        # Test that the operation was registered with inferred name 'testautoname'
        img_pack = ImgPack(Image.new('RGB', (100, 100)))
        result = img_pack.testautoname()
        assert result.context['auto_name_applied'] is True
    
    def test_abstract_apply_method(self):
        """Test that the apply method is abstract and must be implemented."""
        # Attempt to instantiate the abstract base class
        with pytest.raises(TypeError):
            Operation()
        
        # Attempt to instantiate a subclass without implementing apply
        class IncompleteOperation(Operation):
            pass
        
        with pytest.raises(TypeError):
            IncompleteOperation()