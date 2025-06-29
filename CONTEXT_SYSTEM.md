# Pilflow Context System

The Pilflow Context System provides a robust, type-safe way to manage and share data between image processing operations. This system ensures that operations can communicate effectively while maintaining data integrity and providing helpful debugging capabilities.

## Overview

The context system consists of three main components:

1. **ContextData Base Class**: A foundation for creating structured, JSON-serializable context data classes
2. **Registration System**: Automatic registration of context classes with snake_case naming
3. **ImgPack Integration**: Seamless integration with the ImgPack class for context management

## Key Features

- **Type Safety**: Structured context data with validation
- **JSON Serialization**: Full serialization/deserialization support
- **Automatic Registration**: Context classes are automatically registered with inferred names
- **Missing Context Detection**: Automatic detection and logging of missing required contexts
- **Operation Suggestions**: Helpful suggestions for generating missing context data
- **Backward Compatibility**: Works alongside the existing legacy context system

## Basic Usage

### Creating Context Data Classes

```python
from pilflow.core.context import ContextData

@ContextData.register
class MyContextData(ContextData):
    """Custom context data for my operation."""
    
    def validate(self):
        """Validate the context data."""
        if 'required_field' not in self._data:
            raise ValueError("required_field is mandatory")
        
        if self._data['value'] < 0:
            raise ValueError("value must be non-negative")
    
    @property
    def required_field(self):
        return self._data['required_field']
    
    @property
    def value(self):
        return self._data['value']

# Create instance
context = MyContextData(required_field="test", value=42)
print(context.required_field)  # "test"
print(context.value)  # 42
```

### Using with ImgPack

```python
from pilflow import ImgPack
from pilflow.contexts.resolution import ResolutionContextData

# Create ImgPack
img_pack = ImgPack(image)

# Add structured context
resolution_context = ResolutionContextData(
    original_width=1920,
    original_height=1080,
    resolution_category="Full HD",
    aspect_ratio=1920/1080
)
img_pack.add_context(resolution_context)

# Retrieve context
resolution = img_pack.get_context('resolution')
print(f"Resolution: {resolution.original_width}x{resolution.original_height}")
print(f"Is HD: {resolution.is_hd_or_better()}")
```

### JSON Serialization

```python
# Serialize context to JSON
json_str = context.to_json()
print(json_str)  # {"required_field": "test", "value": 42}

# Restore from JSON
restored = MyContextData.from_json(json_str)

# Serialize entire ImgPack with contexts
img_pack_json = img_pack.to_json()
restored_pack = ImgPack.from_json(img_pack_json, image)
```

## Built-in Context Classes

### ResolutionContextData

Stores image resolution information:

```python
from pilflow.contexts.resolution import ResolutionContextData

resolution = ResolutionContextData(
    original_width=1920,
    original_height=1080,
    resolution_category="Full HD",
    aspect_ratio=1920/1080
)

# Properties and methods
print(resolution.total_pixels)  # 2073600
print(resolution.is_4k())       # False
print(resolution.is_hd_or_better())  # True
print(resolution.is_landscape())     # True
```

**Fields:**
- `original_width`: Original image width (int)
- `original_height`: Original image height (int)
- `resolution_category`: Category ("SD", "HD", "Full HD", "4K", "8K", "Other")
- `aspect_ratio`: Image aspect ratio (float)

### ResizeContextData

Stores image resizing information:

```python
from pilflow.contexts.resize import ResizeContextData

resize = ResizeContextData(
    current_width=800,
    current_height=600,
    target_width=1024,
    target_height=768,
    resized=True,
    resize_width=800,
    resize_height=600
)

# Properties and methods
print(resize.current_aspect_ratio)   # 1.333...
print(resize.has_target_dimensions()) # True
print(resize.calculate_scale_factor()) # 1.0
```

**Fields:**
- `current_width`: Current image width (int)
- `current_height`: Current image height (int)
- `target_width`: Target width (int, optional)
- `target_height`: Target height (int, optional)
- `resized`: Whether image was resized (bool)
- `resize_width`: Actual resize width (int, optional)
- `resize_height`: Actual resize height (int, optional)

### BlurContextData

Stores image blur information:

```python
from pilflow.contexts.blur import BlurContextData

blur = BlurContextData(
    blur_applied=True,
    blur_radius=2.5
)

# Properties and methods
print(blur.get_blur_intensity())  # "medium"
print(blur.is_light_blur())       # False
print(blur.is_medium_blur())      # True
```

**Fields:**
- `blur_applied`: Whether blur was applied (bool)
- `blur_radius`: Blur radius value (float)

## Operation Integration

### Reading Context Data

Operations should read from structured context data when available:

```python
@Operation.register
class MyOperation(Operation):
    def apply(self, img_pack):
        # Try to get structured context first
        resolution_context = img_pack.get_context('resolution')
        
        if resolution_context:
            width = resolution_context.original_width
            height = resolution_context.original_height
        else:
            # Fallback to legacy context
            width = img_pack.context.get('original_width')
            height = img_pack.context.get('original_height')
            
            # Log missing context for debugging
            img_pack.log_missing_contexts(['resolution'], 'MyOperation')
        
        # Process image...
        return img_pack.copy(new_img=processed_image)
```

### Writing Context Data

Operations should create structured context data for their outputs:

```python
@Operation.register
class AnalysisOperation(Operation):
    def apply(self, img_pack):
        # Perform analysis...
        
        # Create structured context data
        analysis_context = AnalysisContextData(
            feature_count=len(features),
            confidence=0.95,
            processing_time=elapsed_time
        )
        
        # Create new ImgPack with context
        result = img_pack.copy()
        result.add_context(analysis_context)
        
        return result
```

## Missing Context Detection

The system automatically detects missing contexts and provides helpful suggestions:

```python
# Check for missing contexts
required_contexts = ['resolution', 'resize', 'blur']
missing = img_pack.get_missing_contexts(required_contexts)
print(f"Missing: {missing}")  # ['resize', 'blur']

# Log missing contexts with operation suggestions
img_pack.log_missing_contexts(missing, 'my_operation')
# Output:
# Warning: my_operation requires missing contexts: ['resize', 'blur']
# Suggested operations to generate missing contexts:
#   - Run 'resize' operation to generate 'resize' context
#   - Run 'blur' operation to generate 'blur' context
```

## Advanced Features

### Custom Registration Names

```python
@ContextData.register('custom_name')
class MyContextData(ContextData):
    # Will be registered as 'custom_name' instead of 'my'
    pass
```

### Context Validation

All context classes must implement a `validate()` method:

```python
class StrictContextData(ContextData):
    def validate(self):
        required_fields = ['field1', 'field2']
        for field in required_fields:
            if field not in self._data:
                raise ValueError(f"{field} is required")
        
        if self._data['field1'] < 0:
            raise ValueError("field1 must be non-negative")
```

### Deep Copying

Context data is automatically deep-copied when ImgPack instances are copied:

```python
original_pack = ImgPack(image)
original_pack.add_context(my_context)

copied_pack = original_pack.copy()
# Contexts are deep-copied - modifying one won't affect the other
```

## Best Practices

1. **Always Validate**: Implement comprehensive validation in your context classes
2. **Use Properties**: Provide convenient property accessors for common data
3. **Check for Missing Contexts**: Always check for required contexts and log missing ones
4. **Fallback Gracefully**: Provide fallbacks to legacy context when structured context is missing
5. **Document Fields**: Clearly document all context data fields and their types
6. **Use Descriptive Names**: Choose clear, descriptive names for context classes and fields

## Migration from Legacy Context

The new context system is fully backward compatible. You can migrate gradually:

1. **Phase 1**: Update operations to read from structured contexts with legacy fallback
2. **Phase 2**: Update operations to write structured contexts alongside legacy context
3. **Phase 3**: Remove legacy context dependencies once all operations are updated

```python
# Migration example
def apply(self, img_pack):
    # New: Try structured context first
    resolution_context = img_pack.get_context('resolution')
    if resolution_context:
        width = resolution_context.original_width
    else:
        # Legacy: Fallback to old context
        width = img_pack.context.get('original_width')
        img_pack.log_missing_contexts(['resolution'], self.__class__.__name__)
    
    # ... process image ...
    
    # New: Create structured context
    result_context = MyResultContextData(result_data=data)
    result = img_pack.copy(new_img=new_image)
    result.add_context(result_context)
    
    # Legacy: Also update old context for compatibility
    result.context['result_data'] = data
    
    return result
```

## Examples

See `examples/context_system_demo.py` for a comprehensive demonstration of all context system features.