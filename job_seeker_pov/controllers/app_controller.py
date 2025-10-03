"""
Application Controller - Coordinates between GUI and business logic
"""

from typing import Dict, Any, Optional
from models.profile_manager import ProfileManager
from models.job_analyzer import JobAnalyzer
from models.resume_generator import ResumeGenerator
from views.gui_manager import GUIManager
from utils.export_manager import ExportManager


class AppController:
    """Main application controller that coordinates all components"""
    
    def __init__(self):
        """Initialize the application controller"""
        self.profile_manager = ProfileManager()
        self.job_analyzer = JobAnalyzer()
        self.resume_generator = ResumeGenerator()
        self.export_manager = ExportManager()
        self.gui_manager = GUIManager()
        
        # Application state
        self.current_profile = None
        self.current_job_analysis = None
        self.current_resume = None
        self.current_job_description = None
    
    def start_application(self) -> None:
        """Start the GUI application"""
        try:
            # Load existing profile if available
            self.current_profile = self.profile_manager.load_profile()
            
            # Initialize GUI with controller reference
            self.gui_manager.set_controller(self)
            self.gui_manager.create_main_window()
            
            # Start GUI event loop
            self.gui_manager.run()
            
        except Exception as e:
            print(f"Error starting application: {e}")
            raise
    
    def create_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Create a new user profile"""
        try:
            if self.profile_manager.create_profile(profile_data):
                self.current_profile = profile_data
                return True
            return False
        except Exception as e:
            print(f"Error creating profile: {e}")
            return False
    
    def update_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Update existing user profile"""
        try:
            if self.profile_manager.update_profile(profile_data):
                self.current_profile = profile_data
                return True
            return False
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    
    def load_profile(self) -> Optional[Dict[str, Any]]:
        """Load user profile from storage"""
        try:
            profile = self.profile_manager.load_profile()
            if profile:
                self.current_profile = profile
            return profile
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def analyze_job_description(self, job_description: str) -> Optional[Dict[str, Any]]:
        """Analyze job description and return structured requirements"""
        try:
            if not job_description.strip():
                return None
            
            # Store job description for history tracking
            self.current_job_description = job_description
            
            # Extract keywords and requirements
            keywords = self.job_analyzer.extract_keywords(job_description)
            requirements = self.job_analyzer.identify_requirements(job_description)
            
            # Calculate relevance score if profile exists
            relevance_score = 0.0
            if self.current_profile:
                relevance_score = self.job_analyzer.calculate_relevance_score(
                    self.current_profile, requirements
                )
            
            # Combine results
            analysis = {
                "keywords": keywords,
                "relevance_score": relevance_score,
                **requirements
            }
            
            self.current_job_analysis = analysis
            return analysis
            
        except Exception as e:
            print(f"Error analyzing job description: {e}")
            return None
    
    def generate_resume(self) -> Optional[Dict[str, Any]]:
        """Generate tailored resume based on profile and job analysis"""
        try:
            if not self.current_profile:
                raise ValueError("No profile available for resume generation")
            
            if not self.current_job_analysis:
                raise ValueError("No job analysis available for resume generation")
            
            # Generate resume
            resume_data = self.resume_generator.generate_resume(
                self.current_profile, self.current_job_analysis
            )
            
            self.current_resume = resume_data
            return resume_data
            
        except Exception as e:
            print(f"Error generating resume: {e}")
            return None
    
    def format_resume(self, resume_data: Optional[Dict[str, Any]] = None) -> str:
        """Format resume data into text format"""
        try:
            data_to_format = resume_data or self.current_resume
            if not data_to_format:
                return "No resume data available"
            
            return self.resume_generator.format_resume(data_to_format)
            
        except Exception as e:
            print(f"Error formatting resume: {e}")
            return f"Error formatting resume: {e}"
    
    def export_resume(self, format_type: str = "dialog") -> Optional[str]:
        """Export resume using the export manager"""
        try:
            if not self.current_resume:
                raise ValueError("No resume available for export")
            
            # Get formatted resume content
            resume_content = self.format_resume()
            
            if format_type == "dialog":
                # Show export dialog
                return self.export_manager.show_export_dialog(
                    resume_content, 
                    self.current_profile, 
                    self.current_job_description
                )
            else:
                # Direct export (for programmatic use)
                filename = f"resume_{format_type}"
                if format_type == "pdf":
                    success = self.export_manager.export_to_pdf(
                        resume_content, filename, self.current_profile, self.current_job_description
                    )
                elif format_type == "docx":
                    success = self.export_manager.export_to_docx(
                        resume_content, filename, self.current_profile, self.current_job_description
                    )
                else:
                    success = self.export_manager.export_to_txt(
                        resume_content, filename, self.current_profile, self.current_job_description
                    )
                
                return filename if success else None
            
        except Exception as e:
            print(f"Error exporting resume: {e}")
            return None
    
    def validate_profile(self, profile_data: Dict[str, Any]) -> list:
        """Validate profile data and return any errors"""
        try:
            return self.profile_manager.validate_profile(profile_data)
        except Exception as e:
            print(f"Error validating profile: {e}")
            return [f"Validation error: {e}"]
    
    def get_profile_schema(self) -> Dict[str, Any]:
        """Get the expected profile data schema"""
        return self.profile_manager.get_profile_schema()
    
    def get_resume_history(self) -> list:
        """Get resume export history"""
        try:
            return self.export_manager.get_resume_history()
        except Exception as e:
            print(f"Error getting resume history: {e}")
            return []
    
    def clear_resume_history(self) -> bool:
        """Clear resume export history"""
        try:
            return self.export_manager.clear_history()
        except Exception as e:
            print(f"Error clearing resume history: {e}")
            return False
    
    def delete_history_entry(self, entry_id: str) -> bool:
        """Delete a specific history entry"""
        try:
            return self.export_manager.delete_history_entry(entry_id)
        except Exception as e:
            print(f"Error deleting history entry: {e}")
            return False
    
    def check_export_dependencies(self) -> Dict[str, bool]:
        """Check which export formats are available"""
        return self.export_manager.check_dependencies()
    
    def get_missing_dependencies(self) -> list:
        """Get list of missing export dependencies"""
        return self.export_manager.get_missing_dependencies()
    
    def reset_application_state(self) -> None:
        """Reset all application state"""
        self.current_profile = None
        self.current_job_analysis = None
        self.current_resume = None
        self.current_job_description = None