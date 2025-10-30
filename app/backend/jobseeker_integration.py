import sys
import os
import tempfile
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from job_seeker_pov.models.profile_manager import ProfileManager
    from job_seeker_pov.models.job_analyzer import JobAnalyzer
    from job_seeker_pov.models.resume_generator import ResumeGenerator
    from job_seeker_pov.utils.export_manager import ExportManager
except ImportError as e:
    print(f"Error importing Job Seeker modules: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

class JobSeekerIntegration:
    def __init__(self):
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.profile_manager = ProfileManager(data_dir)
        self.job_analyzer = JobAnalyzer()
        self.resume_generator = ResumeGenerator()
        self.export_manager = ExportManager(data_dir)
        self.current_profile = None
        self.current_analysis = None
        self.current_resume = None
    
    def get_profile(self):
        try:
            profile = self.profile_manager.load_profile()
            self.current_profile = profile
            return {
                'success': True,
                'message': 'Profile loaded successfully' if profile else 'No profile found',
                'data': profile,
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error loading profile',
                'data': None,
                'errors': [str(e)]
            }
    
    def create_profile(self, profile_data):
        try:
            errors = self.profile_manager.validate_profile(profile_data)
            if errors:
                return {
                    'success': False,
                    'message': 'Profile validation failed',
                    'data': None,
                    'errors': errors
                }
            
            success = self.profile_manager.create_profile(profile_data)
            if success:
                self.current_profile = profile_data
                return {
                    'success': True,
                    'message': 'Profile created successfully',
                    'data': profile_data,
                    'errors': []
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to create profile',
                    'data': None,
                    'errors': ['Profile creation failed']
                }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error creating profile',
                'data': None,
                'errors': [str(e)]
            }
    
    def update_profile(self, profile_data):
        try:
            errors = self.profile_manager.validate_profile(profile_data)
            if errors:
                return {
                    'success': False,
                    'message': 'Profile validation failed',
                    'data': None,
                    'errors': errors
                }
            
            success = self.profile_manager.update_profile(profile_data)
            if success:
                self.current_profile = profile_data
                return {
                    'success': True,
                    'message': 'Profile updated successfully',
                    'data': profile_data,
                    'errors': []
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to update profile',
                    'data': None,
                    'errors': ['Profile update failed']
                }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error updating profile',
                'data': None,
                'errors': [str(e)]
            }
    
    def validate_profile(self, profile_data):
        try:
            errors = self.profile_manager.validate_profile(profile_data)
            return {
                'success': len(errors) == 0,
                'message': 'Profile is valid' if len(errors) == 0 else 'Profile validation failed',
                'data': {'valid': len(errors) == 0, 'errors': errors},
                'errors': errors
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error validating profile',
                'data': None,
                'errors': [str(e)]
            }
    
    def analyze_job(self, job_description):
        try:
            if not job_description.strip():
                return {
                    'success': False,
                    'message': 'Job description is required',
                    'data': None,
                    'errors': ['Empty job description']
                }
            
            keywords = self.job_analyzer.extract_keywords(job_description)
            requirements = self.job_analyzer.identify_requirements(job_description)
            
            relevance_score = 0.0
            if self.current_profile:
                relevance_score = self.job_analyzer.calculate_relevance_score(
                    self.current_profile, requirements
                )
            
            analysis = {
                'keywords': keywords,
                'relevance_score': relevance_score,
                **requirements
            }
            
            self.current_analysis = analysis
            
            return {
                'success': True,
                'message': 'Job analysis completed successfully',
                'data': analysis,
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error analyzing job description',
                'data': None,
                'errors': [str(e)]
            }
    
    def generate_resume(self, profile, analysis):
        try:
            if not profile:
                profile = self.current_profile
            if not analysis:
                analysis = self.current_analysis
            
            if not profile:
                return {
                    'success': False,
                    'message': 'Profile is required for resume generation',
                    'data': None,
                    'errors': ['No profile available']
                }
            
            if not analysis:
                return {
                    'success': False,
                    'message': 'Job analysis is required for resume generation',
                    'data': None,
                    'errors': ['No job analysis available']
                }
            
            resume_data = self.resume_generator.generate_resume(profile, analysis)
            formatted_resume = self.resume_generator.format_resume(resume_data)
            
            self.current_resume = {
                'data': resume_data,
                'formatted': formatted_resume
            }
            
            return {
                'success': True,
                'message': 'Resume generated successfully',
                'data': {
                    'resume_data': resume_data,
                    'formatted_resume': formatted_resume
                },
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error generating resume',
                'data': None,
                'errors': [str(e)]
            }
    
    def export_resume(self, content, format_type, profile=None, job_description=None):
        try:
            if not content and self.current_resume:
                content = self.current_resume['formatted']
            
            if not content:
                return {
                    'success': False,
                    'message': 'No resume content available for export',
                    'data': None,
                    'errors': ['No resume content']
                }
            
            if not profile:
                profile = self.current_profile
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = "resume"
            if profile and "personal_info" in profile:
                name = profile["personal_info"].get("name", "").strip()
                if name:
                    default_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
                    default_name = default_name.replace(' ', '_').lower()
            
            filename = f"{default_name}_{timestamp}.{format_type}"
            filepath = os.path.join(tempfile.gettempdir(), filename)
            
            success = False
            if format_type == 'pdf':
                success = self.export_manager.export_to_pdf(content, filepath, profile, job_description)
            elif format_type == 'docx':
                success = self.export_manager.export_to_docx(content, filepath, profile, job_description)
            else:
                success = self.export_manager.export_to_txt(content, filepath, profile, job_description)
            
            if success:
                return {
                    'success': True,
                    'message': 'Resume exported successfully',
                    'data': {
                        'filename': filename,
                        'filepath': filepath,
                        'format': format_type
                    },
                    'errors': []
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to export resume',
                    'data': None,
                    'errors': ['Export operation failed']
                }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error exporting resume',
                'data': None,
                'errors': [str(e)]
            }
    
    def get_history(self):
        try:
            history = self.export_manager.get_resume_history()
            return {
                'success': True,
                'message': 'History retrieved successfully',
                'data': history,
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error retrieving history',
                'data': None,
                'errors': [str(e)]
            }