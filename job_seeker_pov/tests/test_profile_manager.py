"""
Unit tests for ProfileManager class
"""

import unittest
import os
import json
import tempfile
import shutil
from models.profile_manager import ProfileManager


class TestProfileManager(unittest.TestCase):
    """Test cases for ProfileManager functionality"""
    
    def setUp(self):
        """Set up test environment with temporary directory"""
        self.test_dir = tempfile.mkdtemp()
        self.profile_manager = ProfileManager(data_dir=self.test_dir)
        
        # Sample valid profile data
        self.valid_profile = {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0123",
                "address": "123 Main St, City, State 12345",
                "linkedin": "https://linkedin.com/in/johndoe"
            },
            "summary": "Experienced software developer with 5+ years in web development",
            "work_experience": [
                {
                    "company": "Tech Corp",
                    "position": "Senior Developer",
                    "start_date": "2020-01",
                    "end_date": "2023-12",
                    "description": "Led development of web applications",
                    "achievements": ["Improved performance by 40%", "Led team of 3 developers"]
                }
            ],
            "education": [
                {
                    "institution": "University of Technology",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "graduation_date": "2019-05",
                    "gpa": 3.8
                }
            ],
            "skills": {
                "technical": ["Python", "JavaScript", "React", "Django"],
                "soft": ["Leadership", "Communication", "Problem Solving"],
                "languages": ["English", "Spanish"],
                "certifications": ["AWS Certified Developer"]
            },
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Built scalable e-commerce solution",
                    "technologies": ["Python", "Django", "PostgreSQL"],
                    "url": "https://github.com/johndoe/ecommerce"
                }
            ]
        }
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_create_profile_success(self):
        """Test successful profile creation"""
        result = self.profile_manager.create_profile(self.valid_profile)
        self.assertTrue(result)
        
        # Verify file was created
        profile_file = os.path.join(self.test_dir, "profile.json")
        self.assertTrue(os.path.exists(profile_file))
        
        # Verify content
        with open(profile_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data["personal_info"]["name"], "John Doe")
        self.assertIn("created_at", saved_data)
        self.assertIn("updated_at", saved_data)
    
    def test_create_profile_validation_failure(self):
        """Test profile creation with invalid data"""
        invalid_profile = {"personal_info": {"name": ""}}  # Missing required fields
        
        result = self.profile_manager.create_profile(invalid_profile)
        self.assertFalse(result)
        
        # Verify file was not created
        profile_file = os.path.join(self.test_dir, "profile.json")
        self.assertFalse(os.path.exists(profile_file))
    
    def test_load_profile_success(self):
        """Test successful profile loading"""
        # First create a profile
        self.profile_manager.create_profile(self.valid_profile)
        
        # Then load it
        loaded_profile = self.profile_manager.load_profile()
        self.assertIsNotNone(loaded_profile)
        self.assertEqual(loaded_profile["personal_info"]["name"], "John Doe")
        self.assertIn("created_at", loaded_profile)
    
    def test_load_profile_no_file(self):
        """Test loading profile when no file exists"""
        loaded_profile = self.profile_manager.load_profile()
        self.assertIsNone(loaded_profile)
    
    def test_update_profile_success(self):
        """Test successful profile update"""
        # Create initial profile
        self.profile_manager.create_profile(self.valid_profile)
        
        # Update profile
        updated_profile = self.valid_profile.copy()
        updated_profile["personal_info"]["name"] = "Jane Doe"
        
        result = self.profile_manager.update_profile(updated_profile)
        self.assertTrue(result)
        
        # Verify update
        loaded_profile = self.profile_manager.load_profile()
        self.assertEqual(loaded_profile["personal_info"]["name"], "Jane Doe")
        self.assertIn("created_at", loaded_profile)
        self.assertIn("updated_at", loaded_profile)
    
    def test_update_profile_validation_failure(self):
        """Test profile update with invalid data"""
        # Create initial profile
        self.profile_manager.create_profile(self.valid_profile)
        
        # Try to update with invalid data
        invalid_update = {"personal_info": {"email": "invalid-email"}}
        
        result = self.profile_manager.update_profile(invalid_update)
        self.assertFalse(result)
        
        # Verify original profile is unchanged
        loaded_profile = self.profile_manager.load_profile()
        self.assertEqual(loaded_profile["personal_info"]["name"], "John Doe")
    
    def test_delete_profile_success(self):
        """Test successful profile deletion"""
        # Create profile
        self.profile_manager.create_profile(self.valid_profile)
        profile_file = os.path.join(self.test_dir, "profile.json")
        self.assertTrue(os.path.exists(profile_file))
        
        # Delete profile
        result = self.profile_manager.delete_profile()
        self.assertTrue(result)
        self.assertFalse(os.path.exists(profile_file))
    
    def test_delete_profile_no_file(self):
        """Test deleting profile when no file exists"""
        result = self.profile_manager.delete_profile()
        self.assertTrue(result)  # Should succeed even if file doesn't exist
    
    def test_validate_profile_valid_data(self):
        """Test validation with valid profile data"""
        errors = self.profile_manager.validate_profile(self.valid_profile)
        self.assertEqual(len(errors), 0)
    
    def test_validate_profile_missing_required_fields(self):
        """Test validation with missing required fields"""
        invalid_profile = {
            "personal_info": {"name": "John Doe"}
            # Missing email, work_experience, education, skills
        }
        
        errors = self.profile_manager.validate_profile(invalid_profile)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Missing required field" in error for error in errors))
    
    def test_validate_profile_invalid_email(self):
        """Test validation with invalid email format"""
        invalid_profile = self.valid_profile.copy()
        invalid_profile["personal_info"]["email"] = "invalid-email"
        
        errors = self.profile_manager.validate_profile(invalid_profile)
        self.assertTrue(any("Invalid email format" in error for error in errors))
    
    def test_validate_profile_invalid_work_experience(self):
        """Test validation with invalid work experience structure"""
        invalid_profile = self.valid_profile.copy()
        invalid_profile["work_experience"] = [{"company": ""}]  # Missing required fields
        
        errors = self.profile_manager.validate_profile(invalid_profile)
        self.assertTrue(any("Missing required field in work_experience" in error for error in errors))
    
    def test_validate_profile_invalid_education(self):
        """Test validation with invalid education structure"""
        invalid_profile = self.valid_profile.copy()
        invalid_profile["education"] = [{"institution": ""}]  # Missing degree
        
        errors = self.profile_manager.validate_profile(invalid_profile)
        self.assertTrue(any("Missing required field in education" in error for error in errors))
    
    def test_validate_profile_invalid_skills_structure(self):
        """Test validation with invalid skills structure"""
        invalid_profile = self.valid_profile.copy()
        invalid_profile["skills"] = "not a dictionary"
        
        errors = self.profile_manager.validate_profile(invalid_profile)
        self.assertTrue(any("skills must be a dictionary" in error for error in errors))
    
    def test_get_profile_schema(self):
        """Test getting profile schema template"""
        schema = self.profile_manager.get_profile_schema()
        
        # Verify schema structure
        self.assertIn("personal_info", schema)
        self.assertIn("work_experience", schema)
        self.assertIn("education", schema)
        self.assertIn("skills", schema)
        self.assertIn("projects", schema)
        
        # Verify nested structures
        self.assertIn("name", schema["personal_info"])
        self.assertIn("email", schema["personal_info"])
        self.assertIsInstance(schema["work_experience"], list)
        self.assertIsInstance(schema["education"], list)
        self.assertIsInstance(schema["skills"], dict)
    
    def test_data_directory_creation(self):
        """Test that data directory is created if it doesn't exist"""
        # Create ProfileManager with non-existent directory
        new_test_dir = os.path.join(self.test_dir, "new_data_dir")
        self.assertFalse(os.path.exists(new_test_dir))
        
        ProfileManager(data_dir=new_test_dir)
        self.assertTrue(os.path.exists(new_test_dir))


if __name__ == '__main__':
    unittest.main()