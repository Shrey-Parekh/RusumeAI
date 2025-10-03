"""
Unit tests for ResumeGenerator class
"""

import unittest
from models.resume_generator import ResumeGenerator


class TestResumeGenerator(unittest.TestCase):
    """Test cases for ResumeGenerator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = ResumeGenerator()
        
        self.sample_profile = {
            "personal_info": {
                "name": "Jane Smith",
                "email": "jane@example.com",
                "phone": "555-0123",
                "address": "123 Main St, City, State",
                "linkedin": "linkedin.com/in/janesmith"
            },
            "summary": "Experienced software developer with expertise in web technologies",
            "work_experience": [
                {
                    "company": "TechCorp",
                    "position": "Senior Developer",
                    "start_date": "2021",
                    "end_date": "Present",
                    "description": "Lead development of web applications using Python and React",
                    "achievements": [
                        "Improved application performance by 40%",
                        "Led team of 5 developers",
                        "Implemented CI/CD pipeline"
                    ]
                },
                {
                    "company": "StartupXYZ",
                    "position": "Full Stack Developer",
                    "start_date": "2019",
                    "end_date": "2021",
                    "description": "Developed REST APIs and frontend interfaces",
                    "achievements": [
                        "Built scalable microservices architecture",
                        "Reduced load times by 50%"
                    ]
                }
            ],
            "skills": {
                "technical": ["Python", "JavaScript", "React", "Django", "SQL", "AWS"],
                "soft": ["Leadership", "Communication", "Problem Solving"],
                "languages": ["English", "French"],
                "certifications": ["AWS Certified Developer"]
            },
            "education": [
                {
                    "institution": "State University",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "graduation_date": "2019",
                    "gpa": 3.8
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Built full-stack e-commerce solution",
                    "technologies": ["Python", "Django", "React", "PostgreSQL"],
                    "url": "github.com/jane/ecommerce"
                },
                {
                    "name": "Data Analytics Dashboard",
                    "description": "Created real-time analytics dashboard",
                    "technologies": ["Python", "Flask", "D3.js", "MongoDB"],
                    "url": "github.com/jane/analytics"
                }
            ]
        }
        
        self.sample_job_analysis = {
            "required_skills": ["Python", "Django", "SQL", "Git"],
            "preferred_skills": ["AWS", "React", "Docker"],
            "experience_level": "3 years",
            "education_requirements": "bachelor",
            "key_responsibilities": [
                "Develop web applications",
                "Write clean code",
                "Collaborate with team"
            ],
            "company_info": "Leading tech company"
        }
    
    def test_generate_resume_structure(self):
        """Test that generate_resume returns correct structure"""
        resume = self.generator.generate_resume(self.sample_profile, self.sample_job_analysis)
        
        self.assertIsInstance(resume, dict)
        
        # Check required sections
        expected_sections = [
            "personal_info", "summary", "work_experience", 
            "skills", "education", "projects"
        ]
        for section in expected_sections:
            self.assertIn(section, resume)
    
    def test_generate_resume_empty_profile(self):
        """Test generate_resume with empty profile raises error"""
        with self.assertRaises(ValueError):
            self.generator.generate_resume({}, self.sample_job_analysis)
        
        with self.assertRaises(ValueError):
            self.generator.generate_resume(None, self.sample_job_analysis)
    
    def test_prioritize_content_work_experience(self):
        """Test that work experience is prioritized by relevance"""
        job_keywords = ["Python", "Django", "React"]
        prioritized = self.generator.prioritize_content(self.sample_profile, job_keywords)
        
        work_exp = prioritized["work_experience"]
        self.assertIsInstance(work_exp, list)
        self.assertGreater(len(work_exp), 0)
        
        # First experience should be more relevant (contains Python and React)
        first_exp = work_exp[0]
        self.assertIn("Python", first_exp["description"])
        self.assertIn("React", first_exp["description"])
    
    def test_prioritize_content_skills(self):
        """Test that skills are prioritized by job relevance"""
        job_keywords = ["Python", "AWS", "Docker"]
        prioritized = self.generator.prioritize_content(self.sample_profile, job_keywords)
        
        technical_skills = prioritized["skills"]["technical"]
        
        # Python and AWS should be prioritized (they're in job keywords)
        self.assertIn("Python", technical_skills[:3])  # Should be in top 3
        self.assertIn("AWS", technical_skills[:3])
    
    def test_prioritize_content_projects(self):
        """Test that projects are prioritized by relevance"""
        job_keywords = ["Django", "PostgreSQL"]
        prioritized = self.generator.prioritize_content(self.sample_profile, job_keywords)
        
        projects = prioritized["projects"]
        
        # E-commerce project should be first (contains Django and PostgreSQL)
        first_project = projects[0]
        self.assertEqual(first_project["name"], "E-commerce Platform")
    
    def test_prioritize_content_empty_profile(self):
        """Test prioritize_content with empty profile"""
        result = self.generator.prioritize_content({}, ["Python"])
        self.assertEqual(result, {})
        
        result = self.generator.prioritize_content(None, ["Python"])
        self.assertEqual(result, {})
    
    def test_format_resume_basic_structure(self):
        """Test that format_resume produces properly structured text"""
        resume_data = self.generator.generate_resume(self.sample_profile, self.sample_job_analysis)
        formatted = self.generator.format_resume(resume_data)
        
        self.assertIsInstance(formatted, str)
        self.assertGreater(len(formatted), 0)
        
        # Check for key sections
        self.assertIn("JANE SMITH", formatted.upper())
        self.assertIn("PROFESSIONAL SUMMARY", formatted)
        self.assertIn("WORK EXPERIENCE", formatted)
        self.assertIn("SKILLS", formatted)
        self.assertIn("EDUCATION", formatted)
    
    def test_format_resume_contact_info(self):
        """Test that contact information is properly formatted"""
        resume_data = self.generator.generate_resume(self.sample_profile, self.sample_job_analysis)
        formatted = self.generator.format_resume(resume_data)
        
        # Should contain contact information
        self.assertIn("jane@example.com", formatted)
        self.assertIn("555-0123", formatted)
        self.assertIn("linkedin.com/in/janesmith", formatted)
    
    def test_format_resume_work_experience(self):
        """Test work experience formatting"""
        resume_data = self.generator.generate_resume(self.sample_profile, self.sample_job_analysis)
        formatted = self.generator.format_resume(resume_data)
        
        # Should contain work experience details
        self.assertIn("Senior Developer", formatted)
        self.assertIn("TechCorp", formatted)
        self.assertIn("2021", formatted)
        self.assertIn("Present", formatted)
        
        # Should contain achievements
        self.assertIn("Improved application performance", formatted)
    
    def test_format_resume_skills_section(self):
        """Test skills section formatting"""
        resume_data = self.generator.generate_resume(self.sample_profile, self.sample_job_analysis)
        formatted = self.generator.format_resume(resume_data)
        
        # Should contain skills by category
        self.assertIn("Technical:", formatted)
        self.assertIn("Python", formatted)
        self.assertIn("JavaScript", formatted)
        
        self.assertIn("Soft:", formatted)
        self.assertIn("Leadership", formatted)
    
    def test_format_resume_education(self):
        """Test education section formatting"""
        resume_data = self.generator.generate_resume(self.sample_profile, self.sample_job_analysis)
        formatted = self.generator.format_resume(resume_data)
        
        # Should contain education details
        self.assertIn("Bachelor of Science", formatted)
        self.assertIn("Computer Science", formatted)
        self.assertIn("State University", formatted)
        self.assertIn("GPA: 3.8", formatted)  # Should show GPA >= 3.5
    
    def test_format_resume_projects(self):
        """Test projects section formatting"""
        resume_data = self.generator.generate_resume(self.sample_profile, self.sample_job_analysis)
        formatted = self.generator.format_resume(resume_data)
        
        # Should contain project details
        self.assertIn("PROJECTS", formatted)
        self.assertIn("E-commerce Platform", formatted)
        self.assertIn("Technologies:", formatted)
    
    def test_format_resume_empty_data(self):
        """Test format_resume with empty data"""
        formatted = self.generator.format_resume({})
        self.assertEqual(formatted, "")
        
        formatted = self.generator.format_resume(None)
        self.assertEqual(formatted, "")
    
    def test_generate_tailored_summary(self):
        """Test that summary is tailored to job requirements"""
        original_summary = "Software developer with web experience"
        tailored = self.generator._generate_tailored_summary(original_summary, self.sample_job_analysis)
        
        self.assertIsInstance(tailored, str)
        self.assertIn("Software developer", tailored)
        
        # Should enhance with job-relevant skills
        self.assertTrue(
            any(skill in tailored for skill in ["Python", "Django", "SQL"])
        )
    
    def test_generate_work_experience_tailoring(self):
        """Test that work experience is tailored to job"""
        work_exp = self.sample_profile["work_experience"]
        tailored = self.generator._generate_work_experience(work_exp, self.sample_job_analysis)
        
        self.assertIsInstance(tailored, list)
        self.assertGreater(len(tailored), 0)
        
        # Should limit to reasonable number
        self.assertLessEqual(len(tailored), 4)
    
    def test_generate_skills_section_prioritization(self):
        """Test that skills section prioritizes job-relevant skills"""
        skills = self.sample_profile["skills"]
        tailored = self.generator._generate_skills_section(skills, self.sample_job_analysis)
        
        self.assertIsInstance(tailored, dict)
        
        # Technical skills should be prioritized
        technical = tailored.get("technical", [])
        
        # Job-relevant skills should appear first
        job_skills = ["Python", "Django", "SQL"]
        for skill in job_skills:
            if skill in self.sample_profile["skills"]["technical"]:
                # Should be in top positions
                self.assertIn(skill, technical[:5])
    
    def test_optimize_length_basic(self):
        """Test that optimize_length works without errors"""
        resume_data = self.generator.generate_resume(self.sample_profile, self.sample_job_analysis)
        optimized = self.generator._optimize_length(resume_data)
        
        self.assertIsInstance(optimized, dict)
        
        # Should maintain structure
        for key in resume_data:
            self.assertIn(key, optimized)
    
    def test_calculate_experience_relevance(self):
        """Test experience relevance calculation"""
        experience = self.sample_profile["work_experience"][0]
        job_keywords = ["python", "react", "web"]
        
        score = self.generator._calculate_experience_relevance(experience, job_keywords)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        
        # Should have positive score due to matching keywords
        self.assertGreater(score, 0.0)
    
    def test_calculate_skill_relevance(self):
        """Test skill relevance calculation"""
        # Exact match
        score = self.generator._calculate_skill_relevance("Python", ["python"])
        self.assertEqual(score, 1.0)
        
        # No match
        score = self.generator._calculate_skill_relevance("COBOL", ["python"])
        self.assertEqual(score, 0.0)
        
        # Partial match
        score = self.generator._calculate_skill_relevance("JavaScript", ["script"])
        self.assertEqual(score, 1.0)
    
    def test_calculate_project_relevance(self):
        """Test project relevance calculation"""
        project = self.sample_profile["projects"][0]
        job_keywords = ["python", "django", "ecommerce"]
        
        score = self.generator._calculate_project_relevance(project, job_keywords)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        
        # Should have positive score due to matching technologies
        self.assertGreater(score, 0.0)
    
    def test_enhance_description(self):
        """Test description enhancement with job keywords"""
        original = "Developed web applications"
        keywords = ["Python", "Django"]
        
        enhanced = self.generator._enhance_description(original, keywords)
        
        self.assertIsInstance(enhanced, str)
        self.assertIn("Developed web applications", enhanced)
        
        # Should add relevant keywords
        self.assertTrue(
            any(keyword in enhanced for keyword in keywords)
        )
    
    def test_section_priorities(self):
        """Test that section priorities are defined"""
        self.assertIsInstance(self.generator.section_priorities, dict)
        self.assertIn("personal_info", self.generator.section_priorities)
        self.assertIn("work_experience", self.generator.section_priorities)


if __name__ == '__main__':
    unittest.main()