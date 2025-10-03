# Design Document

## Overview

The Unified Resume Platform will integrate the HR Resume Matching system and Job Seeker Resume Tailoring application into a single Flask-based web interface. The design focuses on creating a seamless, professional user experience while preserving all existing backend functionalities through a clean integration layer.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web Application                     │
├─────────────────────────────────────────────────────────────┤
│  Unified Frontend (HTML/CSS/JavaScript)                     │
│  ├── Navigation Component                                   │
│  ├── HR Mode Interface                                      │
│  ├── Job Seeker Mode Interface                             │
│  └── Shared Components (Forms, Modals, etc.)               │
├─────────────────────────────────────────────────────────────┤
│  Flask Integration Layer                                     │
│  ├── Route Handlers                                        │
│  ├── Data Transformation                                   │
│  └── Response Formatting                                   │
├─────────────────────────────────────────────────────────────┤
│  Existing Backend Systems (Preserved)                       │
│  ├── HR Matching Engine                                    │
│  │   ├── ResumeMatcher                                     │
│  │   ├── TF-IDF Processing                                 │
│  │   └── Skill Extraction                                  │
│  └── Job Seeker System                                     │
│      ├── ProfileManager                                    │
│      ├── JobAnalyzer                                       │
│      ├── ResumeGenerator                                   │
│      └── ExportManager                                     │
└─────────────────────────────────────────────────────────────┘
```

### Integration Strategy

The design follows a facade pattern where the Flask application acts as a unified interface layer over the existing backend systems. No modifications will be made to the core business logic of either system.

## Components and Interfaces

### 1. Flask Application Structure

```
unified_resume_platform/
├── app.py                    # Main Flask application
├── templates/
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Landing page with mode selection
│   ├── hr_dashboard.html    # HR functionality interface
│   └── jobseeker_dashboard.html # Job seeker interface
├── static/
│   ├── css/
│   │   └── style.css        # Unified styling
│   └── js/
│       └── app.js           # Frontend interactions
├── backend/
│   ├── hr_integration.py    # HR system integration
│   └── jobseeker_integration.py # Job seeker integration
└── requirements.txt         # Dependencies
```

### 2. Navigation Component

**Purpose**: Provide seamless switching between HR and Job Seeker modes

**Features**:
- Mode toggle (HR/Job Seeker)
- Feature navigation within each mode
- User context awareness
- Responsive design

**Interface**:
```python
class NavigationHandler:
    def get_navigation_context(mode: str) -> dict
    def validate_mode_access(mode: str) -> bool
```

### 3. HR Integration Component

**Purpose**: Integrate existing HR matching functionality into the web interface

**Features**:
- Resume and job description input forms
- Sample data loading
- Match analysis display
- Results visualization

**Interface**:
```python
class HRIntegration:
    def analyze_match(resume_text: str, job_description: str) -> dict
    def get_sample_data() -> dict
    def get_sample_content(type: str, name: str) -> dict
```

### 4. Job Seeker Integration Component

**Purpose**: Integrate job seeker functionality into the web interface

**Features**:
- Profile management forms
- Job analysis interface
- Resume generation and preview
- Export functionality
- History management

**Interface**:
```python
class JobSeekerIntegration:
    def manage_profile(action: str, data: dict) -> dict
    def analyze_job(job_description: str) -> dict
    def generate_resume(profile: dict, analysis: dict) -> dict
    def export_resume(content: str, format: str) -> str
    def get_history() -> list
```

## Data Models

### 1. Unified Response Format

All API responses will follow a consistent format:

```python
{
    "success": bool,
    "data": dict,
    "message": str,
    "errors": list
}
```

### 2. HR Match Analysis Response

```python
{
    "match_score": float,
    "resume_skills": list,
    "jd_skills": list,
    "matching_skills": list,
    "missing_skills": list,
    "skill_match_percentage": float
}
```

### 3. Job Analysis Response

```python
{
    "keywords": list,
    "required_skills": list,
    "preferred_skills": list,
    "experience_level": str,
    "education_requirements": str,
    "relevance_score": float
}
```

### 4. Profile Data Structure

Maintains the existing job seeker profile structure:

```python
{
    "personal_info": dict,
    "summary": str,
    "work_experience": list,
    "education": list,
    "skills": dict,
    "projects": list
}
```

## Error Handling

### 1. Client-Side Error Handling

- Form validation with real-time feedback
- Network error handling with retry mechanisms
- User-friendly error messages
- Loading states and progress indicators

### 2. Server-Side Error Handling

- Input validation and sanitization
- Backend system error catching
- Graceful degradation for missing features
- Comprehensive logging for debugging

### 3. Error Response Format

```python
{
    "success": false,
    "data": null,
    "message": "User-friendly error message",
    "errors": ["Detailed error 1", "Detailed error 2"]
}
```

## Testing Strategy

### 1. Integration Testing

- Test HR matching functionality through web interface
- Test job seeker profile management through web interface
- Test resume generation and export through web interface
- Test navigation and mode switching

### 2. Frontend Testing

- Cross-browser compatibility testing
- Responsive design testing
- User interaction testing
- Form validation testing

### 3. Backend Integration Testing

- Verify preservation of existing functionality
- Test data flow between frontend and backend systems
- Validate response formats and error handling
- Performance testing under load

## User Interface Design

### 1. Design Principles

- **Consistency**: Unified visual language across all features
- **Clarity**: Clear information hierarchy and intuitive navigation
- **Efficiency**: Streamlined workflows for common tasks
- **Accessibility**: WCAG 2.1 compliant design
- **Responsiveness**: Mobile-first responsive design

### 2. Visual Design System

**Color Palette**:
- Primary: Professional blue (#2c3e50)
- Secondary: Accent blue (#3498db)
- Success: Green (#27ae60)
- Warning: Orange (#f39c12)
- Error: Red (#e74c3c)
- Neutral: Gray scale (#ecf0f1 to #2c3e50)

**Typography**:
- Headers: 'Segoe UI', system fonts
- Body: 'Segoe UI', system fonts
- Code: 'Courier New', monospace

**Layout**:
- Grid-based responsive layout
- Consistent spacing using 8px base unit
- Card-based component design
- Sticky navigation header

### 3. Component Library

**Forms**:
- Consistent input styling
- Real-time validation feedback
- Progressive disclosure for complex forms
- Auto-save functionality where appropriate

**Data Display**:
- Responsive tables
- Interactive charts for match scores
- Collapsible sections for detailed information
- Export buttons with format options

**Navigation**:
- Breadcrumb navigation
- Tab-based feature switching
- Mobile-friendly hamburger menu
- Context-aware navigation items

## Security Considerations

### 1. Input Validation

- Server-side validation for all inputs
- XSS prevention through proper escaping
- CSRF protection for form submissions
- File upload restrictions and validation

### 2. Data Protection

- Secure handling of personal information
- No persistent storage of sensitive data
- Secure file export mechanisms
- Session management for user context

### 3. Access Control

- Mode-based feature access
- Input sanitization and validation
- Rate limiting for API endpoints
- Secure error handling without information leakage

## Performance Optimization

### 1. Frontend Performance

- Minified CSS and JavaScript
- Lazy loading for large forms
- Efficient DOM manipulation
- Optimized image assets

### 2. Backend Performance

- Efficient integration with existing systems
- Caching for frequently accessed data
- Asynchronous processing where appropriate
- Optimized file handling for exports

### 3. Network Optimization

- Compressed responses
- Efficient API design
- Minimal payload sizes
- Progressive loading for large datasets

## Deployment Architecture

### 1. Application Structure

- Single Flask application serving all functionality
- Static file serving through Flask
- Template-based rendering with Jinja2
- RESTful API endpoints for dynamic functionality

### 2. Dependencies

- Flask framework with essential extensions
- Existing backend system dependencies
- Frontend libraries (minimal, prefer vanilla JS)
- Export libraries (reportlab, python-docx)

### 3. Configuration

- Environment-based configuration
- Configurable paths for backend systems
- Debug and production modes
- Logging configuration

## Integration Points

### 1. HR System Integration

The Flask application will import and utilize the existing HR matching engine:

```python
from hr_part.matching_engine import ResumeMatcher
from hr_part.sample_data import SAMPLE_RESUMES, SAMPLE_JOB_DESCRIPTIONS
```

### 2. Job Seeker System Integration

The Flask application will import and utilize the existing job seeker components:

```python
from job_seeker_pov.models.profile_manager import ProfileManager
from job_seeker_pov.models.job_analyzer import JobAnalyzer
from job_seeker_pov.models.resume_generator import ResumeGenerator
from job_seeker_pov.utils.export_manager import ExportManager
```

### 3. Data Flow

- HTTP requests → Flask routes → Backend systems → Response formatting → JSON/HTML response
- File uploads → Validation → Backend processing → Results display
- Export requests → Backend generation → File download response

This design ensures a seamless integration while preserving all existing functionality and providing a superior user experience through the unified web interface.