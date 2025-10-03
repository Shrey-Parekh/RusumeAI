"""
Unit tests for JobAnalyzer class
"""

import unittest
from models.job_analyzer import JobAnalyzer


class TestJobAnalyzer(unittest.TestCase):
    """Test cases for JobAnalyzer functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = JobAnalyzer()
        
        self.sample_job_description = """
        Software Engineer - Python Developer
        
        We are looking for a skilled Python developer to join our team.
        
        Required Skills:
        - 3+ years of Python experience
        - Experience with Django or Flask
        - SQL database knowledge
        - Git version control
        
        Preferred Skills:
        - AWS cloud experience
        - Docker containerization
        - React frontend development
        
        Responsibilities:
        • Develop and maintain web applications
        • Write clean, maintainable code
        • Collaborate with cross-functional teams
        • Participate in code reviews
        
        Education:
        Bachelor's degree in Computer Science or related field
        """
        
        self.sample_profile = {
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "skills": {
                "technical": ["Python", "Django", "SQL", "Git", "AWS"],
                "soft": ["Communication", "Problem Solving"],
                "languages": ["English", "Spanish"],
                "certifications": ["AWS Certified"]
            },
            "work_experience": [
                {
                    "company": "Tech Corp",
                    "position": "Software Developer",
                    "start_date": "2020",
                    "description": "Developed Python web applications using Django"
                },
                {
                    "company": "StartupXYZ",
                    "position": "Junior Developer",
                    "start_date": "2018",
                    "description": "Built REST APIs with Flask"
                }
            ],
            "education": [
                {
                    "institution": "University",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science"
                }
            ]
        }
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction"""
        keywords = self.analyzer.extract_keywords(self.sample_job_description)
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        
        # Check for expected technical keywords
        keywords_lower = [k.lower() for k in keywords]
        self.assertIn("python", keywords_lower)
        self.assertIn("sql", keywords_lower)
        self.assertIn("git", keywords_lower)
    
    def test_extract_keywords_empty_input(self):
        """Test keyword extraction with empty input"""
        keywords = self.analyzer.extract_keywords("")
        self.assertEqual(keywords, [])
        
        keywords = self.analyzer.extract_keywords(None)
        self.assertEqual(keywords, [])
    
    def test_extract_keywords_filters_stopwords(self):
        """Test that stopwords are filtered out"""
        keywords = self.analyzer.extract_keywords("the quick brown fox and the lazy dog")
        
        # Should not contain common stopwords
        keywords_lower = [k.lower() for k in keywords]
        self.assertNotIn("the", keywords_lower)
        self.assertNotIn("and", keywords_lower)
    
    def test_identify_requirements_structure(self):
        """Test that identify_requirements returns correct structure"""
        requirements = self.analyzer.identify_requirements(self.sample_job_description)
        
        self.assertIsInstance(requirements, dict)
        
        # Check required keys
        expected_keys = [
            "required_skills", "preferred_skills", "experience_level",
            "education_requirements", "key_responsibilities", "company_info"
        ]
        for key in expected_keys:
            self.assertIn(key, requirements)
    
    def test_identify_requirements_skills_extraction(self):
        """Test extraction of required and preferred skills"""
        requirements = self.analyzer.identify_requirements(self.sample_job_description)
        
        required_skills = requirements["required_skills"]
        preferred_skills = requirements["preferred_skills"]
        
        self.assertIsInstance(required_skills, list)
        self.assertIsInstance(preferred_skills, list)
        
        # Check for expected skills (case-insensitive)
        required_lower = [skill.lower() for skill in required_skills]
        preferred_lower = [skill.lower() for skill in preferred_skills]
        
        # Should find some technical skills
        self.assertTrue(any("python" in skill for skill in required_lower))
        self.assertTrue(any("aws" in skill for skill in preferred_lower))
    
    def test_identify_requirements_experience_level(self):
        """Test extraction of experience level"""
        requirements = self.analyzer.identify_requirements(self.sample_job_description)
        
        experience_level = requirements["experience_level"]
        self.assertIsInstance(experience_level, str)
        
        # Should extract "3 years" from "3+ years"
        self.assertIn("3", experience_level)
    
    def test_identify_requirements_empty_input(self):
        """Test identify_requirements with empty input"""
        requirements = self.analyzer.identify_requirements("")
        
        # Should return default structure
        self.assertEqual(requirements["required_skills"], [])
        self.assertEqual(requirements["preferred_skills"], [])
        self.assertEqual(requirements["experience_level"], "")
    
    def test_calculate_relevance_score_high_match(self):
        """Test relevance score calculation with high match"""
        requirements = self.analyzer.identify_requirements(self.sample_job_description)
        score = self.analyzer.calculate_relevance_score(self.sample_profile, requirements)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        
        # Should be relatively high score due to matching skills
        self.assertGreater(score, 0.5)
    
    def test_calculate_relevance_score_no_match(self):
        """Test relevance score with no matching profile"""
        empty_profile = {
            "personal_info": {"name": "Test", "email": "test@example.com"},
            "skills": {"technical": ["COBOL", "Fortran"]},
            "work_experience": [],
            "education": []
        }
        
        requirements = self.analyzer.identify_requirements(self.sample_job_description)
        score = self.analyzer.calculate_relevance_score(empty_profile, requirements)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        
        # Should be low score due to no matching skills
        self.assertLess(score, 0.3)
    
    def test_calculate_relevance_score_empty_inputs(self):
        """Test relevance score with empty inputs"""
        score = self.analyzer.calculate_relevance_score({}, {})
        self.assertEqual(score, 0.0)
        
        score = self.analyzer.calculate_relevance_score(None, {})
        self.assertEqual(score, 0.0)
        
        score = self.analyzer.calculate_relevance_score({}, None)
        self.assertEqual(score, 0.0)
    
    def test_skill_patterns_recognition(self):
        """Test that skill patterns correctly identify technical skills"""
        test_text = "Experience with Python, JavaScript, AWS, Docker, and machine learning"
        keywords = self.analyzer.extract_keywords(test_text)
        
        keywords_lower = [k.lower() for k in keywords]
        
        # Should recognize technical skills
        self.assertIn("python", keywords_lower)
        self.assertIn("javascript", keywords_lower)
        self.assertIn("aws", keywords_lower)
        self.assertIn("docker", keywords_lower)
        self.assertIn("machine learning", keywords_lower)
    
    def test_experience_patterns_recognition(self):
        """Test that experience patterns are correctly identified"""
        test_descriptions = [
            "5+ years of experience required",
            "Minimum 3 years experience",
            "2-4 years of relevant experience",
            "At least 7 years experience"
        ]
        
        for desc in test_descriptions:
            requirements = self.analyzer.identify_requirements(desc)
            experience_level = requirements["experience_level"]
            
            # Should extract some numeric value
            self.assertTrue(any(char.isdigit() for char in experience_level))
    
    def test_education_patterns_recognition(self):
        """Test that education requirements are identified"""
        test_text = "Bachelor's degree in Computer Science required"
        requirements = self.analyzer.identify_requirements(test_text)
        
        education_req = requirements["education_requirements"].lower()
        self.assertIn("bachelor", education_req)


if __name__ == '__main__':
    unittest.main()