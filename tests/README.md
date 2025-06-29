# Pilflow Tests

This directory contains tests for the pilflow package.

## Test Structure

- `test_data/`: Contains utilities for managing test image data
- `core/`: Tests for core components (ImgPack, Operation)
- `operations/`: Tests for individual operations (resize, blur, etc.)
- `test_integration.py`: Integration tests for the entire package

## Running Tests

### Prerequisites

Install the development dependencies:

```bash
pip install -e ".[dev]"
```

### Running All Tests

```bash
python -m pytest
```

### Running Tests with Coverage

```bash
python -m pytest --cov=pilflow
```

### Running Specific Tests

```bash
python -m pytest tests/core/test_image_pack.py
```

## Test Data Management

The tests use a data management system that automatically downloads test images when needed. The images are stored in a temporary directory (`/tmp/pilflow_test_data`) to avoid interfering with the workspace.

The test data is automatically cleaned up after all tests are run.

## Adding New Tests

When adding new tests:

1. For testing core functionality, add tests to the appropriate file in `tests/core/`
2. For testing operations, add tests to the appropriate file in `tests/operations/`
3. For testing integration between components, add tests to `test_integration.py`

## Creating Custom Test Fixtures

If you need additional test fixtures, add them to `conftest.py`.