import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from hr.matching_engine import ResumeMatcher
    from hr.sample_data import SAMPLE_RESUMES, SAMPLE_JOB_DESCRIPTIONS
except ImportError as e:
    print(f"Error importing HR modules: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

class HRIntegration:
    def __init__(self):
        self.matcher = ResumeMatcher()
    
    def analyze_match(self, resume_text, job_description):
        try:
            if not resume_text or not job_description:
                return {
                    'success': False,
                    'message': 'Resume and job description are required',
                    'data': None,
                    'errors': ['Missing required input']
                }
            
            analysis = self.matcher.get_match_analysis(resume_text, job_description)
            
            return {
                'success': True,
                'message': 'Match analysis completed successfully',
                'data': analysis,
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error analyzing match',
                'data': None,
                'errors': [str(e)]
            }
    
    def get_sample_data(self):
        try:
            return {
                'success': True,
                'message': 'Sample data retrieved successfully',
                'data': {
                    'resumes': list(SAMPLE_RESUMES.keys()),
                    'job_descriptions': list(SAMPLE_JOB_DESCRIPTIONS.keys())
                },
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error retrieving sample data',
                'data': None,
                'errors': [str(e)]
            }
    
    def get_sample_content(self, sample_type, name):
        try:
            if sample_type == 'resume':
                content = SAMPLE_RESUMES.get(name, '')
            elif sample_type == 'job_description':
                content = SAMPLE_JOB_DESCRIPTIONS.get(name, '')
            else:
                return {
                    'success': False,
                    'message': 'Invalid sample type',
                    'data': None,
                    'errors': ['Sample type must be "resume" or "job_description"']
                }
            
            if not content:
                return {
                    'success': False,
                    'message': 'Sample not found',
                    'data': None,
                    'errors': [f'Sample "{name}" not found']
                }
            
            return {
                'success': True,
                'message': 'Sample content retrieved successfully',
                'data': {'content': content},
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error retrieving sample content',
                'data': None,
                'errors': [str(e)]
            }