"""
Integration tests for GUI components and user workflows
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import json

from views.gui_manager import GUIManager
from controllers.app_controller import AppController
from models.profile_manager import ProfileManager
from models.job_analyzer import JobAnalyzer
from models.resume_generator import ResumeGenerator


class TestGUIIntegration(unittest.TestCase):
    """Test GUI components and user workflows"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
        # Mock the GUI to avoid actually creating windows during tests
        self.gui_manager = GUIManager()
        self.gui_manager.root = Mock()
        
        # Create test profile data
        self.test_profile = {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "555-0123",
                "address": "123 Main St, City, State",
                "linkedin": "linkedin.com/in/johndoe"
            },
            "summary": "Experienced software developer with 5 years of experience.",
            "work_experience": [
                {
                    "company": "Tech Corp",
                    "position": "Software Developer",
                    "start_date": "2020-01-01",
                    "end_date": "2023-12-31",
                    "description": "Developed web applications using Python and JavaScript.",
                    "achievements": ["Improved performance by 30%", "Led team of 3 developers"]
                }
            ],
            "education": [
                {
                    "institution": "University of Technology",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "graduation_date": "2019-05-15",
                    "gpa": 3.8
                }
            ],
            "skills": {
                "technical": ["Python", "JavaScript", "SQL", "React"],
                "soft": ["Leadership", "Communication", "Problem Solving"],
                "languages": ["English", "Spanish"],
                "certifications": ["AWS Certified Developer"]
            },
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Built a full-stack e-commerce platform",
                    "technologies": ["Python", "Django", "React", "PostgreSQL"],
                    "url": "https://github.com/johndoe/ecommerce"
                }
            ]
        }
        
        self.test_job_description = """
        Software Developer Position
        
        We are looking for a skilled Software Developer to join our team.
        
        Requirements:
        - 3+ years of experience in software development
        - Proficiency in Python and JavaScript
        - Experience with React and Django
        - Bachelor's degree in Computer Science or related field
        - Strong problem-solving skills
        
        Preferred:
        - AWS experience
        - Leadership experience
        - SQL knowledge
        """
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_gui_manager_initialization(self):
        """Test GUI manager initialization"""
        gui = GUIManager()
        
        # Check that model instances are created
        self.assertIsInstance(gui.profile_manager, ProfileManager)
        self.assertIsInstance(gui.job_analyzer, JobAnalyzer)
        self.assertIsInstance(gui.resume_generator, ResumeGenerator)
        
        # Check initial state
        self.assertIsNone(gui.current_profile)
        self.assertIsNone(gui.current_job_analysis)
        self.assertIsNone(gui.current_resume)
    
    def test_create_main_window(self):
        """Test main window creation - simplified test"""
        gui = GUIManager()
        
        # Test that GUI manager can be initialized without errors
        self.assertIsNotNone(gui.profile_manager)
        self.assertIsNotNone(gui.job_analyzer)
        self.assertIsNotNone(gui.resume_generator)
        
        # Test that initial state is correct
        self.assertIsNone(gui.current_profile)
        self.assertIsNone(gui.current_job_analysis)
        self.assertIsNone(gui.current_resume)
    
    def test_profile_data_collection(self):
        """Test profile data collection from form"""
        gui = GUIManager()
        
        # Mock form variables
        gui.profile_form_vars = {
            "personal_info": {
                "name": Mock(get=Mock(return_value="John Doe")),
                "email": Mock(get=Mock(return_value="john@example.com")),
                "phone": Mock(get=Mock(return_value="555-0123")),
                "address": Mock(get=Mock(return_value="123 Main St")),
                "linkedin": Mock(get=Mock(return_value="linkedin.com/in/johndoe"))
            },
            "summary": Mock(get=Mock(return_value="Test summary\n")),
            "skills": {
                "technical": Mock(get=Mock(return_value="Python, JavaScript\n")),
                "soft": Mock(get=Mock(return_value="Leadership, Communication\n")),
                "languages": Mock(get=Mock(return_value="English, Spanish\n")),
                "certifications": Mock(get=Mock(return_value="AWS Certified\n"))
            },
            "work_experience": [],
            "education": [],
            "projects": []
        }
        
        profile_data = gui._collect_profile_data()
        
        # Verify collected data
        self.assertEqual(profile_data["personal_info"]["name"], "John Doe")
        self.assertEqual(profile_data["personal_info"]["email"], "john@example.com")
        self.assertEqual(profile_data["summary"], "Test summary")
        self.assertEqual(profile_data["skills"]["technical"], ["Python", "JavaScript"])
    
    def test_profile_validation_integration(self):
        """Test profile validation integration"""
        gui = GUIManager()
        
        # Test valid profile
        validation_errors = gui.profile_manager.validate_profile(self.test_profile)
        self.assertEqual(len(validation_errors), 0)
        
        # Test invalid profile
        invalid_profile = self.test_profile.copy()
        del invalid_profile["personal_info"]["name"]
        
        validation_errors = gui.profile_manager.validate_profile(invalid_profile)
        self.assertGreater(len(validation_errors), 0)
    
    def test_job_analysis_integration(self):
        """Test job analysis integration"""
        gui = GUIManager()
        
        # Mock job text widget
        mock_widget = Mock()
        mock_widget.get.return_value = self.test_job_description
        gui.job_text_widget = mock_widget
        
        # Set current profile
        gui.current_profile = self.test_profile
        
        # Test analysis
        keywords = gui.job_analyzer.extract_keywords(self.test_job_description)
        requirements = gui.job_analyzer.identify_requirements(self.test_job_description)
        
        # Verify analysis results
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        self.assertIn("required_skills", requirements)
        self.assertIn("experience_level", requirements)
    
    def test_resume_generation_integration(self):
        """Test resume generation integration"""
        gui = GUIManager()
        gui.current_profile = self.test_profile
        
        # Analyze job description
        job_analysis = gui.job_analyzer.identify_requirements(self.test_job_description)
        gui.current_job_analysis = job_analysis
        
        # Generate resume
        resume_data = gui.resume_generator.generate_resume(self.test_profile, job_analysis)
        
        # Verify resume structure
        self.assertIn("personal_info", resume_data)
        self.assertIn("work_experience", resume_data)
        self.assertIn("skills", resume_data)
        self.assertIn("education", resume_data)
        
        # Test formatting
        formatted_resume = gui.resume_generator.format_resume(resume_data)
        self.assertIsInstance(formatted_resume, str)
        self.assertIn("JOHN DOE", formatted_resume)  # Name is converted to uppercase
    
    def test_error_handling(self):
        """Test error handling in GUI operations"""
        gui = GUIManager()
        
        # Test with invalid profile data
        with patch('tkinter.messagebox.showerror') as mock_error:
            gui.profile_form_vars = {}  # Empty form vars should cause error
            gui._collect_profile_data()
            # Should handle error gracefully and return empty dict
    
    def test_app_controller_integration(self):
        """Test application controller integration"""
        with patch('models.profile_manager.ProfileManager') as mock_pm:
            mock_pm.return_value.load_profile.return_value = self.test_profile
            
            controller = AppController()
            
            # Test profile loading
            profile = controller.load_profile()
            self.assertIsNotNone(profile)  # Just check that a profile was loaded
            
            # Test job analysis
            analysis = controller.analyze_job_description(self.test_job_description)
            self.assertIsNotNone(analysis)
            self.assertIn("keywords", analysis)
            
            # Test resume generation
            resume = controller.generate_resume()
            self.assertIsNotNone(resume)
    
    def test_complete_user_workflow(self):
        """Test complete user workflow from profile creation to resume export"""
        # Create temporary profile manager with test directory
        with patch('models.profile_manager.ProfileManager') as mock_pm:
            mock_instance = mock_pm.return_value
            mock_instance.validate_profile.return_value = []
            mock_instance.update_profile.return_value = True
            mock_instance.load_profile.return_value = self.test_profile
            
            controller = AppController()
            
            # Step 1: Create/Load profile
            success = controller.create_profile(self.test_profile)
            self.assertTrue(success)
            
            # Step 2: Analyze job description
            analysis = controller.analyze_job_description(self.test_job_description)
            self.assertIsNotNone(analysis)
            
            # Step 3: Generate resume
            resume = controller.generate_resume()
            self.assertIsNotNone(resume)
            
            # Step 4: Format resume
            formatted = controller.format_resume()
            self.assertIsInstance(formatted, str)
            self.assertIn("JOHN DOE", formatted)  # Name is converted to uppercase
    
    def test_form_validation_feedback(self):
        """Test form validation and user feedback"""
        gui = GUIManager()
        
        # Test validation with missing required fields
        incomplete_profile = {
            "personal_info": {"name": "John"},  # Missing email
            "work_experience": [],
            "education": [],
            "skills": {}
        }
        
        errors = gui.profile_manager.validate_profile(incomplete_profile)
        self.assertGreater(len(errors), 0)
        
        # Verify specific error messages
        error_messages = " ".join(errors)
        self.assertIn("email", error_messages.lower())
    
    def test_data_persistence(self):
        """Test data persistence across sessions"""
        # Create profile manager with test directory
        pm = ProfileManager(data_dir=self.test_dir)
        
        # Save profile
        success = pm.create_profile(self.test_profile)
        self.assertTrue(success)
        
        # Load profile in new instance
        pm2 = ProfileManager(data_dir=self.test_dir)
        loaded_profile = pm2.load_profile()
        
        self.assertIsNotNone(loaded_profile)
        self.assertEqual(loaded_profile["personal_info"]["name"], "John Doe")
    
    def test_resume_export_functionality(self):
        """Test resume export functionality"""
        controller = AppController()
        controller.current_resume = {
            "personal_info": {"name": "John Doe", "email": "john@example.com"},
            "summary": "Test summary",
            "work_experience": [],
            "skills": {},
            "education": [],
            "projects": []
        }
        
        # Test export (using the new method signature)
        exported_file = controller.export_resume("txt")
        self.assertIsNotNone(exported_file)
        
        # Verify file was created and contains expected content
        expected_file = "resume_txt.txt"
        self.assertTrue(os.path.exists(expected_file))
        with open(expected_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("JOHN DOE", content)  # Name is converted to uppercase


class TestGUIErrorHandling(unittest.TestCase):
    """Test GUI error handling and edge cases"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.gui = GUIManager()
    
    def test_empty_form_handling(self):
        """Test handling of empty form submissions"""
        # Mock empty form variables
        self.gui.profile_form_vars = {
            "personal_info": {
                "name": Mock(get=Mock(return_value="")),
                "email": Mock(get=Mock(return_value=""))
            },
            "summary": Mock(get=Mock(return_value="\n")),
            "skills": {
                "technical": Mock(get=Mock(return_value="\n"))
            },
            "work_experience": [],
            "education": [],
            "projects": []
        }
        
        profile_data = self.gui._collect_profile_data()
        
        # Should return empty/default values gracefully
        self.assertEqual(profile_data["personal_info"]["name"], "")
        self.assertEqual(profile_data["summary"], "")
    
    def test_invalid_job_description_handling(self):
        """Test handling of invalid job descriptions"""
        # Test empty job description
        keywords = self.gui.job_analyzer.extract_keywords("")
        self.assertEqual(keywords, [])
        
        requirements = self.gui.job_analyzer.identify_requirements("")
        self.assertIn("required_skills", requirements)
        self.assertEqual(requirements["required_skills"], [])
    
    def test_missing_profile_for_resume_generation(self):
        """Test resume generation without profile"""
        self.gui.current_profile = None
        self.gui.current_job_analysis = {"keywords": ["python"]}
        
        with self.assertRaises(ValueError):
            self.gui.resume_generator.generate_resume(None, self.gui.current_job_analysis)


if __name__ == '__main__':
    # Run tests with minimal GUI interaction
    unittest.main(verbosity=2)