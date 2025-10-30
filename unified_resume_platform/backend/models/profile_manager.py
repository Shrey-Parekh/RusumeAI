"""
Profile Manager - Handles user profile CRUD operations with JSON persistence
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class ProfileManager:
    """Manages user profile data with JSON-based persistence"""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize ProfileManager with data directory"""
        self.data_dir = data_dir
        self.profile_file = os.path.join(data_dir, "profile.json")
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def create_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Create a new profile with validation"""
        try:
            # Validate profile data
            validation_errors = self.validate_profile(profile_data)
            if validation_errors:
                raise ValueError(f"Profile validation failed: {', '.join(validation_errors)}")
            
            # Add metadata
            profile_data["created_at"] = datetime.now().isoformat()
            profile_data["updated_at"] = datetime.now().isoformat()
            
            # Save to file
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error creating profile: {e}")
            return False
    
    def load_profile(self) -> Optional[Dict[str, Any]]:
        """Load existing profile from file"""
        try:
            if not os.path.exists(self.profile_file):
                return None
                
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
                
            return profile_data
            
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def update_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Update existing profile with validation"""
        try:
            # Validate profile data
            validation_errors = self.validate_profile(profile_data)
            if validation_errors:
                raise ValueError(f"Profile validation failed: {', '.join(validation_errors)}")
            
            # Preserve creation date if it exists
            existing_profile = self.load_profile()
            if existing_profile and "created_at" in existing_profile:
                profile_data["created_at"] = existing_profile["created_at"]
            
            # Update timestamp
            profile_data["updated_at"] = datetime.now().isoformat()
            
            # Save to file
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    
    def delete_profile(self) -> bool:
        """Delete existing profile"""
        try:
            if os.path.exists(self.profile_file):
                os.remove(self.profile_file)
            return True
            
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False
    
    def validate_profile(self, profile_data: Dict[str, Any]) -> List[str]:
        """Validate profile data against schema"""
        errors = []
        
        # Check required top-level fields
        required_fields = ["personal_info", "work_experience", "education", "skills"]
        for field in required_fields:
            if field not in profile_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate personal_info
        if "personal_info" in profile_data:
            personal_info = profile_data["personal_info"]
            required_personal = ["name", "email"]
            for field in required_personal:
                if field not in personal_info or not personal_info[field]:
                    errors.append(f"Missing required personal info: {field}")
            
            # Validate email format (basic)
            if "email" in personal_info and personal_info["email"]:
                email = personal_info["email"]
                if "@" not in email or "." not in email:
                    errors.append("Invalid email format")
        
        # Validate work_experience structure
        if "work_experience" in profile_data:
            work_exp = profile_data["work_experience"]
            if not isinstance(work_exp, list):
                errors.append("work_experience must be a list")
            else:
                for i, exp in enumerate(work_exp):
                    if not isinstance(exp, dict):
                        errors.append(f"work_experience[{i}] must be a dictionary")
                        continue
                    
                    required_exp_fields = ["company", "position", "start_date"]
                    for field in required_exp_fields:
                        if field not in exp or not exp[field]:
                            errors.append(f"Missing required field in work_experience[{i}]: {field}")
        
        # Validate education structure
        if "education" in profile_data:
            education = profile_data["education"]
            if not isinstance(education, list):
                errors.append("education must be a list")
            else:
                for i, edu in enumerate(education):
                    if not isinstance(edu, dict):
                        errors.append(f"education[{i}] must be a dictionary")
                        continue
                    
                    required_edu_fields = ["institution", "degree"]
                    for field in required_edu_fields:
                        if field not in edu or not edu[field]:
                            errors.append(f"Missing required field in education[{i}]: {field}")
        
        # Validate skills structure
        if "skills" in profile_data:
            skills = profile_data["skills"]
            if not isinstance(skills, dict):
                errors.append("skills must be a dictionary")
            else:
                expected_skill_types = ["technical", "soft", "languages", "certifications"]
                for skill_type in expected_skill_types:
                    if skill_type in skills and not isinstance(skills[skill_type], list):
                        errors.append(f"skills.{skill_type} must be a list")
        
        return errors
    
    def get_profile_schema(self) -> Dict[str, Any]:
        """Get the expected profile schema structure"""
        return {
            "personal_info": {
                "name": "",
                "email": "",
                "phone": "",
                "address": "",
                "linkedin": ""
            },
            "summary": "",
            "work_experience": [
                {
                    "company": "",
                    "position": "",
                    "start_date": "",
                    "end_date": "",
                    "description": "",
                    "achievements": []
                }
            ],
            "education": [
                {
                    "institution": "",
                    "degree": "",
                    "field": "",
                    "graduation_date": "",
                    "gpa": 0.0
                }
            ],
            "skills": {
                "technical": [],
                "soft": [],
                "languages": [],
                "certifications": []
            },
            "projects": [
                {
                    "name": "",
                    "description": "",
                    "technologies": [],
                    "url": ""
                }
            ]
        }