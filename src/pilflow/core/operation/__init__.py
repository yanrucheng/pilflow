"""Operation module for pilflow.

This module provides the base classes for all operations in the pilflow pipeline:
- BaseOperation: Abstract base class for all operations
- Operation: ImgPack in, ImgPack out (registered with ImgPack)
- Producer: Any input, ImgPack out (standalone)
- Consumer: ImgPack in, any output (standalone)
"""

from .base import BaseOperation
from .operation import Operation
from .producer import Producer
from .consumer import Consumer

__all__ = [
    'BaseOperation',
    'Operation', 
    'Producer',
    'Consumer'
]