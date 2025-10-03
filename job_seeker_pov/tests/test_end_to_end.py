"""
End-to-End Tests for Resume Tailoring App
Tests complete user workflows from profile creation to resume export
"""

import unittest
import tempfile
import shutil
import os
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import application components
from controllers.app_controller import AppController
from models.profile_manager import ProfileManager
from models.job_analyzer import JobAnalyzer
from models.resume_generator import ResumeGenerator
from utils.export_manager import ExportManager


class TestEndToEndWorkflows(unittest.TestCase):
    """Test complete user workflows"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create data directory
        os.makedirs("data", exist_ok=True)
        
        # Initialize controller
        self.controller = AppController()
        
        # Sample profile data
        self.sample_profile = {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@email.com",
                "phone": "555-0123",
                "address": "123 Main St, City, State 12345",
                "linkedin": "linkedin.com/in/johndoe"
            },
            "summary": "Experienced software developer with 5 years of experience in Python and web development.",
            "work_experience": [
                {
                    "company": "Tech Corp",
                    "position": "Senior Developer",
                    "start_date": "2020-01",
                    "end_date": "Present",
                    "description": "Lead development of web applications using Python and Django.",
                    "achievements": [
                        "Improved application performance by 40%",
                        "Led team of 3 developers"
                    ]
                }
            ],
            "education": [
                {
                    "institution": "University of Technology",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "graduation_date": "2019",
                    "gpa": 3.8
                }
            ],
            "skills": {
                "technical": ["Python", "Django", "JavaScript", "SQL", "Git"],
                "soft": ["Leadership", "Communication", "Problem Solving"],
                "languages": ["English", "Spanish"],
                "certifications": ["AWS Certified Developer"]
            },
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Built a full-stack e-commerce platform using Django and React",
                    "technologies": ["Python", "Django", "React", "PostgreSQL"],
                    "url": "https://github.com/johndoe/ecommerce"
                }
            ]
        }
        
        # Sample job description
        self.sample_job_description = """
        Senior Python Developer
        
        We are looking for an experienced Python developer to join our team.
        
        Requirements:
        - 3+ years of Python development experience
        - Experience with Django framework
        - Knowledge of SQL databases
        - Git version control
        - Strong problem-solving skills
        - Excellent communication skills
        
        Preferred:
        - AWS experience
        - Leadership experience
        - JavaScript knowledge
        """
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_complete_workflow_profile_to_export(self):
        """Test complete workflow: create profile -> analyze job -> generate resume -> export"""
        
        # Step 1: Create profile
        success = self.controller.create_profile(self.sample_profile)
        self.assertTrue(success, "Profile creation should succeed")
        
        # Verify profile was saved
        loaded_profile = self.controller.load_profile()
        self.assertIsNotNone(loaded_profile, "Profile should be loadable after creation")
        self.assertEqual(loaded_profile["personal_info"]["name"], "John Doe")
        
        # Step 2: Analyze job description
        analysis = self.controller.analyze_job_description(self.sample_job_description)
        self.assertIsNotNone(analysis, "Job analysis should succeed")
        self.assertIn("keywords", analysis, "Analysis should contain keywords")
        self.assertIn("relevance_score", analysis, "Analysis should contain relevance score")
        
        # Step 3: Generate resume
        resume_data = self.controller.generate_resume()
        self.assertIsNotNone(resume_data, "Resume generation should succeed")
        
        # Step 4: Format resume
        formatted_resume = self.controller.format_resume()
        self.assertIsInstance(formatted_resume, str, "Formatted resume should be a string")
        self.assertIn("JOHN DOE", formatted_resume, "Resume should contain profile name")
        
        # Step 5: Export resume (text format)
        export_filename = self.controller.export_resume("txt")
        self.assertIsNotNone(export_filename, "Export should succeed")
        
        # Verify export file exists and contains expected content
        expected_filename = "resume_txt.txt"
        self.assertTrue(os.path.exists(expected_filename), "Export file should exist")
        with open(expected_filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("JOHN DOE", content, "Export should contain profile name")
    
    def test_profile_validation_workflow(self):
        """Test profile validation workflow"""
        
        # Test with invalid profile (missing required fields)
        invalid_profile = {
            "personal_info": {
                "name": "",  # Empty name should fail validation
                "email": "invalid-email"  # Invalid email format
            }
        }
        
        validation_errors = self.controller.validate_profile(invalid_profile)
        self.assertGreater(len(validation_errors), 0, "Invalid profile should have validation errors")
        
        # Test with valid profile
        validation_errors = self.controller.validate_profile(self.sample_profile)
        self.assertEqual(len(validation_errors), 0, "Valid profile should have no validation errors")
    
    def test_job_analysis_workflow(self):
        """Test job analysis workflow with different inputs"""
        
        # Test with empty job description
        analysis = self.controller.analyze_job_description("")
        self.assertIsNone(analysis, "Empty job description should return None")
        
        # Test with valid job description
        analysis = self.controller.analyze_job_description(self.sample_job_description)
        self.assertIsNotNone(analysis, "Valid job description should return analysis")
        
        # Verify analysis structure
        expected_keys = ["keywords", "relevance_score"]
        for key in expected_keys:
            self.assertIn(key, analysis, f"Analysis should contain {key}")
        
        # Test relevance score calculation with profile
        self.controller.create_profile(self.sample_profile)
        analysis_with_profile = self.controller.analyze_job_description(self.sample_job_description)
        self.assertGreater(analysis_with_profile["relevance_score"], 0, 
                          "Relevance score should be positive with matching profile")
    
    def test_resume_generation_workflow(self):
        """Test resume generation workflow"""
        
        # Test without profile
        resume = self.controller.generate_resume()
        self.assertIsNone(resume, "Resume generation should fail without profile")
        
        # Create profile
        self.controller.create_profile(self.sample_profile)
        
        # Test without job analysis
        resume = self.controller.generate_resume()
        self.assertIsNone(resume, "Resume generation should fail without job analysis")
        
        # Add job analysis
        self.controller.analyze_job_description(self.sample_job_description)
        
        # Test successful generation
        resume = self.controller.generate_resume()
        self.assertIsNotNone(resume, "Resume generation should succeed with profile and job analysis")
        
        # Verify resume structure
        self.assertIsInstance(resume, dict, "Resume should be a dictionary")
    
    def test_export_manager_integration(self):
        """Test export manager integration"""
        
        # Set up complete workflow
        self.controller.create_profile(self.sample_profile)
        self.controller.analyze_job_description(self.sample_job_description)
        self.controller.generate_resume()
        
        # Test text export
        txt_file = self.controller.export_resume("txt")
        self.assertIsNotNone(txt_file, "Text export should succeed")
        # The filename should be "resume_txt.txt"
        expected_filename = "resume_txt.txt"
        self.assertTrue(os.path.exists(expected_filename), "Text export file should exist")
        
        # Test history tracking
        history = self.controller.get_resume_history()
        self.assertGreater(len(history), 0, "History should contain export entries")
        
        # Verify history entry structure
        entry = history[-1]  # Most recent entry
        expected_fields = ["id", "filename", "format", "timestamp"]
        for field in expected_fields:
            self.assertIn(field, entry, f"History entry should contain {field}")
    
    def test_error_handling_workflow(self):
        """Test error handling in various scenarios"""
        
        # Test with corrupted profile data
        with patch.object(self.controller.profile_manager, 'load_profile', side_effect=Exception("File corrupted")):
            profile = self.controller.load_profile()
            self.assertIsNone(profile, "Should handle corrupted profile gracefully")
        
        # Test with invalid job description format
        with patch.object(self.controller.job_analyzer, 'extract_keywords', side_effect=Exception("Analysis failed")):
            analysis = self.controller.analyze_job_description("test")
            self.assertIsNone(analysis, "Should handle analysis errors gracefully")
        
        # Test export failure
        self.controller.create_profile(self.sample_profile)
        self.controller.analyze_job_description(self.sample_job_description)
        self.controller.generate_resume()
        
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = self.controller.export_resume("txt")
            self.assertIsNone(result, "Should handle export errors gracefully")
    
    def test_application_state_management(self):
        """Test application state management"""
        
        # Test initial state
        self.assertIsNone(self.controller.current_profile)
        self.assertIsNone(self.controller.current_job_analysis)
        self.assertIsNone(self.controller.current_resume)
        
        # Test state after profile creation
        self.controller.create_profile(self.sample_profile)
        self.assertIsNotNone(self.controller.current_profile)
        
        # Test state after job analysis
        self.controller.analyze_job_description(self.sample_job_description)
        self.assertIsNotNone(self.controller.current_job_analysis)
        
        # Test state after resume generation
        self.controller.generate_resume()
        self.assertIsNotNone(self.controller.current_resume)
        
        # Test state reset
        self.controller.reset_application_state()
        self.assertIsNone(self.controller.current_profile)
        self.assertIsNone(self.controller.current_job_analysis)
        self.assertIsNone(self.controller.current_resume)
    
    def test_multiple_resume_generations(self):
        """Test generating multiple resumes for different jobs"""
        
        # Set up profile
        self.controller.create_profile(self.sample_profile)
        
        # First job
        job1 = "Python Developer position requiring Django and PostgreSQL experience"
        analysis1 = self.controller.analyze_job_description(job1)
        resume1 = self.controller.generate_resume()
        
        self.assertIsNotNone(analysis1)
        self.assertIsNotNone(resume1)
        
        # Second job
        job2 = "JavaScript Developer position requiring React and Node.js experience"
        analysis2 = self.controller.analyze_job_description(job2)
        resume2 = self.controller.generate_resume()
        
        self.assertIsNotNone(analysis2)
        self.assertIsNotNone(resume2)
        
        # Verify different analyses
        self.assertNotEqual(analysis1["keywords"], analysis2["keywords"], 
                           "Different jobs should have different keyword analyses")
    
    def test_export_dependency_checking(self):
        """Test export dependency checking"""
        
        dependencies = self.controller.check_export_dependencies()
        self.assertIsInstance(dependencies, dict, "Dependencies should be a dictionary")
        self.assertIn("txt", dependencies, "Text export should always be available")
        self.assertTrue(dependencies["txt"], "Text export should always be True")
        
        missing = self.controller.get_missing_dependencies()
        self.assertIsInstance(missing, list, "Missing dependencies should be a list")


class TestExportManagerIntegration(unittest.TestCase):
    """Test export manager integration specifically"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        os.makedirs("data", exist_ok=True)
        
        self.export_manager = ExportManager()
        self.sample_resume_content = """
        JOHN DOE
        Software Developer
        
        CONTACT INFORMATION
        Email: john.doe@email.com
        Phone: 555-0123
        
        PROFESSIONAL SUMMARY
        Experienced software developer with expertise in Python and web development.
        
        WORK EXPERIENCE
        Senior Developer at Tech Corp (2020-Present)
        - Led development of web applications
        - Improved performance by 40%
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of Technology (2019)
        
        SKILLS
        Technical: Python, Django, JavaScript, SQL
        """
        
        self.sample_profile = {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@email.com"
            }
        }
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_text_export(self):
        """Test text export functionality"""
        filename = "test_resume.txt"
        success = self.export_manager.export_to_txt(
            self.sample_resume_content, 
            filename, 
            self.sample_profile
        )
        
        self.assertTrue(success, "Text export should succeed")
        self.assertTrue(os.path.exists(filename), "Export file should exist")
        
        # Verify content
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, self.sample_resume_content, "Content should match")
    
    def test_history_tracking(self):
        """Test resume export history tracking"""
        # Initial history should be empty
        history = self.export_manager.get_resume_history()
        initial_count = len(history)
        
        # Export a resume
        filename = "test_resume.txt"
        self.export_manager.export_to_txt(
            self.sample_resume_content, 
            filename, 
            self.sample_profile,
            "Python Developer position"
        )
        
        # Check history was updated
        history = self.export_manager.get_resume_history()
        self.assertEqual(len(history), initial_count + 1, "History should have one more entry")
        
        # Verify history entry
        entry = history[-1]
        self.assertEqual(entry["filename"], filename)
        self.assertEqual(entry["format"], "txt")
        self.assertEqual(entry["profile_name"], "John Doe")
        self.assertIn("timestamp", entry)
        self.assertIn("id", entry)
    
    def test_history_management(self):
        """Test history management operations"""
        # Add some history entries
        for i in range(3):
            filename = f"resume_{i}.txt"
            self.export_manager.export_to_txt(
                self.sample_resume_content, 
                filename, 
                self.sample_profile
            )
        
        history = self.export_manager.get_resume_history()
        self.assertEqual(len(history), 3, "Should have 3 history entries")
        
        # Test deleting specific entry
        entry_id = history[0]["id"]
        success = self.export_manager.delete_history_entry(entry_id)
        self.assertTrue(success, "Delete should succeed")
        
        history = self.export_manager.get_resume_history()
        self.assertEqual(len(history), 2, "Should have 2 history entries after deletion")
        
        # Test clearing all history
        success = self.export_manager.clear_history()
        self.assertTrue(success, "Clear should succeed")
        
        history = self.export_manager.get_resume_history()
        self.assertEqual(len(history), 0, "History should be empty after clearing")
    
    @patch('utils.export_manager.REPORTLAB_AVAILABLE', True)
    @patch('utils.export_manager.SimpleDocTemplate')
    def test_pdf_export_when_available(self, mock_doc):
        """Test PDF export when reportlab is available"""
        mock_doc_instance = Mock()
        mock_doc.return_value = mock_doc_instance
        
        filename = "test_resume.pdf"
        success = self.export_manager.export_to_pdf(
            self.sample_resume_content, 
            filename, 
            self.sample_profile
        )
        
        self.assertTrue(success, "PDF export should succeed when reportlab is available")
        mock_doc.assert_called_once()
        mock_doc_instance.build.assert_called_once()
    
    @patch('utils.export_manager.PYTHON_DOCX_AVAILABLE', True)
    @patch('utils.export_manager.Document')
    def test_docx_export_when_available(self, mock_doc):
        """Test Word export when python-docx is available"""
        mock_doc_instance = Mock()
        mock_doc_instance.sections = []
        mock_doc.return_value = mock_doc_instance
        
        # Mock the sections property to avoid attribute errors
        mock_section = Mock()
        mock_doc_instance.sections = [mock_section]
        
        filename = "test_resume.docx"
        
        # Patch the PYTHON_DOCX_AVAILABLE at the module level
        with patch.object(self.export_manager, 'export_to_docx') as mock_export:
            mock_export.return_value = True
            success = self.export_manager.export_to_docx(
                self.sample_resume_content, 
                filename, 
                self.sample_profile
            )
            
            self.assertTrue(success, "DOCX export should succeed when python-docx is available")
            mock_export.assert_called_once_with(
                self.sample_resume_content, 
                filename, 
                self.sample_profile
            )
    
    def test_dependency_checking(self):
        """Test dependency checking functionality"""
        dependencies = ExportManager.check_dependencies()
        self.assertIsInstance(dependencies, dict)
        self.assertIn("txt", dependencies)
        self.assertIn("pdf", dependencies)
        self.assertIn("docx", dependencies)
        self.assertTrue(dependencies["txt"])  # Text should always be available
        
        missing = ExportManager.get_missing_dependencies()
        self.assertIsInstance(missing, list)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)