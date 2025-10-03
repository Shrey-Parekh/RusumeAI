# Unified Resume Platform

A professional Flask-based web application that integrates HR Resume Matching and Job Seeker Resume Tailoring functionalities into a single, unified interface.

## Features

### HR Tools
- Advanced AI-powered resume matching with job descriptions
- Skill gap analysis and compatibility scoring
- Sample data for testing and demonstration
- Interactive results visualization

### Job Seeker Tools
- Comprehensive profile management system
- Job description analysis with keyword extraction
- Intelligent resume generation tailored to specific jobs
- Multi-format export (PDF, Word, Text)
- Export history tracking

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Test imports (optional but recommended):
```bash
python test_imports.py
```

3. Run the application:
```bash
python run.py
```
   Or alternatively:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
unified_resume_platform/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── backend/                        # Integration layer
│   ├── __init__.py
│   ├── hr_integration.py          # HR system wrapper
│   └── jobseeker_integration.py   # Job seeker system wrapper
├── templates/                      # HTML templates
│   ├── __init__.py
│   ├── base.html                  # Base template with navigation
│   ├── index.html                 # Landing page
│   ├── hr_dashboard.html          # HR tools interface
│   └── jobseeker_dashboard.html   # Job seeker interface
├── static/                         # Static assets
│   ├── __init__.py
│   ├── css/
│   │   └── style.css              # Unified styling
│   └── js/
│       └── app.js                 # Frontend interactions
└── data/                          # Data storage
    └── .gitkeep
```

## API Endpoints

### HR Endpoints
- `POST /api/hr/match` - Analyze resume-job compatibility
- `GET /api/hr/samples` - Get available sample data
- `GET /api/hr/sample/<type>/<name>` - Get specific sample content

### Job Seeker Endpoints
- `GET/POST/PUT /api/jobseeker/profile` - Profile management
- `POST /api/jobseeker/analyze` - Job description analysis
- `POST /api/jobseeker/generate` - Resume generation
- `POST /api/jobseeker/export` - Resume export
- `GET /api/jobseeker/history` - Export history
- `POST /api/jobseeker/validate` - Profile validation

## Technology Stack

- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI/ML**: scikit-learn, NLTK, TF-IDF vectorization
- **Export**: ReportLab (PDF), python-docx (Word)
- **Data**: JSON-based persistence

## Key Features

### Unified Interface
- Single navigation between HR and Job Seeker modes
- Consistent design language and user experience
- Responsive design for desktop and mobile

### HR Matching Engine
- Advanced text analysis using TF-IDF and cosine similarity
- Skill extraction and gap analysis
- Detailed compatibility scoring and visualization

### Job Seeker Tools
- Comprehensive profile management with validation
- Intelligent job analysis with keyword extraction
- Resume generation optimized for specific job requirements
- Multi-format export with history tracking

### Professional Design
- Modern, clean interface with professional styling
- Interactive components with smooth animations
- Comprehensive error handling and user feedback
- Mobile-responsive design

## Usage

### For HR Professionals
1. Navigate to "HR Tools" from the main menu
2. Input resume text and job description
3. Use sample data for quick testing
4. Click "Analyze Match" to get detailed compatibility results
5. Review match scores, skill gaps, and recommendations

### For Job Seekers
1. Navigate to "Job Seeker" from the main menu
2. Create/update your professional profile in the "Profile Management" tab
3. Analyze job descriptions in the "Job Analysis" tab
4. Generate tailored resumes in the "Resume Generation" tab
5. Export resumes in multiple formats and track history

## Integration Architecture

The application uses a facade pattern where Flask serves as a unified interface layer over the existing HR and Job Seeker systems. All original business logic is preserved without modification, ensuring reliability and accuracy.

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Performance

- Optimized frontend assets with efficient loading
- Responsive design with mobile-first approach
- Efficient API design with minimal payload sizes
- Cached processing for improved performance