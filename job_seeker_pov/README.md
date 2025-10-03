# Resume Tailoring App

A Python desktop application that helps job seekers create tailored resumes based on specific job descriptions.

## Project Structure

```
resume-tailoring-app/
├── main.py                     # Main application entry point
├── demo_profile_manager.py     # Demo script for ProfileManager
├── README.md                   # Project documentation
├── models/                     # Data models and business logic
│   ├── __init__.py
│   └── profile_manager.py      # Profile CRUD operations with JSON persistence
├── views/                      # GUI components (Tkinter)
│   └── __init__.py
├── controllers/                # Application controllers
│   └── __init__.py
├── utils/                      # Utility functions
│   └── __init__.py
├── data/                       # Data storage directory
│   └── .gitkeep
└── tests/                      # Unit tests
    ├── __init__.py
    └── test_profile_manager.py  # ProfileManager unit tests
```

## Features Implemented

### Task 1: Core Data Models and Profile Management System ✅

- **ProfileManager Class**: Complete CRUD operations for user profiles
  - Create new profiles with validation
  - Load existing profiles from JSON storage
  - Update profiles with data validation
  - Delete profiles
  - Comprehensive data validation with detailed error messages

- **Data Persistence**: JSON-based storage system
  - Automatic data directory creation
  - UTF-8 encoding support
  - Metadata tracking (created_at, updated_at timestamps)

- **Profile Schema**: Structured data model supporting:
  - Personal information (name, email, phone, address, LinkedIn)
  - Professional summary
  - Work experience with achievements
  - Education history
  - Skills (technical, soft, languages, certifications)
  - Projects portfolio

- **Validation System**: Comprehensive data validation
  - Required field validation
  - Email format validation
  - Data type validation for complex structures
  - Detailed error reporting

## Usage

### Running Tests

```bash
# Using pytest
python -m pytest tests/test_profile_manager.py -v

# Using unittest
python -m unittest tests.test_profile_manager -v
```

### Demo

```bash
python demo_profile_manager.py
```

### Basic Usage Example

```python
from models.profile_manager import ProfileManager

# Initialize ProfileManager
pm = ProfileManager()

# Create a profile
profile_data = {
    "personal_info": {
        "name": "John Doe",
        "email": "john@example.com"
    },
    "work_experience": [...],
    "education": [...],
    "skills": {...}
}

# Create profile
success = pm.create_profile(profile_data)

# Load profile
profile = pm.load_profile()

# Update profile
pm.update_profile(updated_data)

# Validate profile
errors = pm.validate_profile(profile_data)
```

## Requirements Satisfied

This implementation satisfies the following requirements from the specification:

- **Requirement 1.1**: Profile management interface foundation
- **Requirement 1.2**: Input and storage of comprehensive profile data
- **Requirement 1.3**: Local data persistence
- **Requirement 1.4**: Profile data loading on application restart
- **Requirement 1.5**: Automatic profile change saving

## Testing

The ProfileManager class includes comprehensive unit tests covering:

- Profile creation with valid and invalid data
- Profile loading and error handling
- Profile updates and validation
- Profile deletion
- Data validation edge cases
- Schema structure verification
- Directory creation and file handling

All tests pass successfully, ensuring robust functionality.

## Next Steps

The core data models and profile management system is complete. The next tasks will involve:

1. Building job analysis and resume generation engine
2. Developing Tkinter GUI interface
3. Implementing export functionality

## Dependencies

- Python 3.7+
- Standard library modules: `json`, `os`, `datetime`, `typing`
- Testing: `unittest` (built-in) or `pytest`