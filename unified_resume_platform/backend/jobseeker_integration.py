import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from job_seeker_pov.models.job_analyzer import JobAnalyzer
    from .db_manager import DatabaseManager
except ImportError as e:
    print(f"Error importing Job Seeker modules: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

class JobSeekerIntegration:
    def __init__(self):
        self.job_analyzer = JobAnalyzer()
        self.db_manager = DatabaseManager()
        self.current_analysis = None

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

            analysis = {
                'keywords': keywords,
                'relevance_score': 0.0,
                **requirements
            }

            self.current_analysis = analysis

            # Try to save to database (optional - won't fail if DB is unavailable)
            try:
                if self.db_manager.connect():
                    self.db_manager.save_job_analysis(job_description, analysis)
                    self.db_manager.disconnect()
            except Exception as db_error:
                print(f"⚠ Database save failed (continuing without DB): {db_error}")

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