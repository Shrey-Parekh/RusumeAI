#!/usr/bin/env python3
"""
Demo script for ProfileManager functionality
"""

from models.profile_manager import ProfileManager


def main():
    """Demonstrate ProfileManager functionality"""
    print("=== Resume Tailoring App - ProfileManager Demo ===\n")
    
    # Initialize ProfileManager
    pm = ProfileManager()
    
    # Sample profile data
    sample_profile = {
        "personal_info": {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "phone": "+1-555-0199",
            "address": "456 Oak Ave, Tech City, CA 94000",
            "linkedin": "https://linkedin.com/in/alicejohnson"
        },
        "summary": "Full-stack developer with 3+ years experience in modern web technologies",
        "work_experience": [
            {
                "company": "StartupXYZ",
                "position": "Full Stack Developer",
                "start_date": "2021-06",
                "end_date": "Present",
                "description": "Developed and maintained web applications using React and Node.js",
                "achievements": [
                    "Reduced page load time by 50%",
                    "Implemented CI/CD pipeline",
                    "Mentored 2 junior developers"
                ]
            }
        ],
        "education": [
            {
                "institution": "State University",
                "degree": "Bachelor of Science",
                "field": "Software Engineering",
                "graduation_date": "2021-05",
                "gpa": 3.7
            }
        ],
        "skills": {
            "technical": ["JavaScript", "Python", "React", "Node.js", "PostgreSQL"],
            "soft": ["Team Collaboration", "Problem Solving", "Agile Development"],
            "languages": ["English", "French"],
            "certifications": ["Google Cloud Professional Developer"]
        },
        "projects": [
            {
                "name": "Task Management App",
                "description": "Built a collaborative task management application",
                "technologies": ["React", "Node.js", "MongoDB"],
                "url": "https://github.com/alicejohnson/task-app"
            }
        ]
    }
    
    # Demo 1: Create profile
    print("1. Creating new profile...")
    success = pm.create_profile(sample_profile)
    print(f"   Profile created: {success}\n")
    
    # Demo 2: Load profile
    print("2. Loading profile...")
    loaded_profile = pm.load_profile()
    if loaded_profile:
        print(f"   Profile loaded for: {loaded_profile['personal_info']['name']}")
        print(f"   Email: {loaded_profile['personal_info']['email']}")
        print(f"   Skills: {len(loaded_profile['skills']['technical'])} technical skills\n")
    
    # Demo 3: Update profile
    print("3. Updating profile...")
    sample_profile["personal_info"]["phone"] = "+1-555-0200"
    sample_profile["skills"]["technical"].append("Docker")
    success = pm.update_profile(sample_profile)
    print(f"   Profile updated: {success}\n")
    
    # Demo 4: Validation
    print("4. Testing validation...")
    invalid_profile = {"personal_info": {"name": ""}}
    errors = pm.validate_profile(invalid_profile)
    print(f"   Validation errors found: {len(errors)}")
    for error in errors[:3]:  # Show first 3 errors
        print(f"   - {error}")
    if len(errors) > 3:
        print(f"   ... and {len(errors) - 3} more errors\n")
    else:
        print()
    
    # Demo 5: Schema
    print("5. Getting profile schema...")
    schema = pm.get_profile_schema()
    print(f"   Schema has {len(schema)} main sections:")
    for section in schema.keys():
        print(f"   - {section}")
    print()
    
    print("=== Demo Complete ===")


if __name__ == "__main__":
    main()