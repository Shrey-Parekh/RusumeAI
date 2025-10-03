#!/usr/bin/env python3
"""
Demo script showing JobAnalyzer and ResumeGenerator functionality
"""

from models.job_analyzer import JobAnalyzer
from models.resume_generator import ResumeGenerator
from models.profile_manager import ProfileManager


def main():
    """Demonstrate job analysis and resume generation"""
    
    # Sample job description
    job_description = """
    Senior Python Developer - Remote
    
    We are seeking an experienced Python developer to join our growing team.
    
    Required Skills:
    - 5+ years of Python development experience
    - Strong experience with Django or Flask frameworks
    - Proficiency in SQL and database design
    - Experience with Git version control
    - Knowledge of REST API development
    
    Preferred Skills:
    - AWS cloud platform experience
    - Docker containerization
    - React or Vue.js frontend experience
    - Experience with microservices architecture
    
    Responsibilities:
    • Design and develop scalable web applications
    • Write clean, maintainable, and well-tested code
    • Collaborate with cross-functional teams
    • Participate in code reviews and technical discussions
    • Mentor junior developers
    
    Requirements:
    Bachelor's degree in Computer Science or related field
    """
    
    # Load sample profile
    profile_manager = ProfileManager()
    profile = profile_manager.load_profile()
    
    if not profile:
        print("No profile found. Please run demo_profile_manager.py first to create a profile.")
        return
    
    print("=== JOB ANALYSIS AND RESUME GENERATION DEMO ===\n")
    
    # Initialize analyzers
    job_analyzer = JobAnalyzer()
    resume_generator = ResumeGenerator()
    
    # Analyze job description
    print("1. ANALYZING JOB DESCRIPTION...")
    print("-" * 40)
    
    keywords = job_analyzer.extract_keywords(job_description)
    print(f"Top Keywords: {', '.join(keywords[:10])}")
    
    requirements = job_analyzer.identify_requirements(job_description)
    print(f"\nRequired Skills: {', '.join(requirements['required_skills'])}")
    print(f"Preferred Skills: {', '.join(requirements['preferred_skills'])}")
    print(f"Experience Level: {requirements['experience_level']}")
    print(f"Education: {requirements['education_requirements']}")
    
    # Calculate relevance score
    relevance_score = job_analyzer.calculate_relevance_score(profile, requirements)
    print(f"\nProfile Relevance Score: {relevance_score:.2f} ({relevance_score*100:.1f}%)")
    
    # Generate tailored resume
    print("\n2. GENERATING TAILORED RESUME...")
    print("-" * 40)
    
    resume_data = resume_generator.generate_resume(profile, requirements)
    formatted_resume = resume_generator.format_resume(resume_data)
    
    print("Generated Resume:")
    print("=" * 60)
    print(formatted_resume)
    print("=" * 60)
    
    # Show prioritization
    print("\n3. CONTENT PRIORITIZATION ANALYSIS...")
    print("-" * 40)
    
    prioritized_content = resume_generator.prioritize_content(profile, keywords)
    
    if "skills" in prioritized_content and "technical" in prioritized_content["skills"]:
        top_skills = prioritized_content["skills"]["technical"][:5]
        print(f"Top Prioritized Technical Skills: {', '.join(top_skills)}")
    
    if "work_experience" in prioritized_content:
        top_experience = prioritized_content["work_experience"][0]
        print(f"Most Relevant Experience: {top_experience.get('position', 'N/A')} at {top_experience.get('company', 'N/A')}")
    
    print(f"\nResume Length: {len(formatted_resume.split())} words, {len(formatted_resume.split(chr(10)))} lines")
    
    print("\n=== DEMO COMPLETE ===")


if __name__ == "__main__":
    main()