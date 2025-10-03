#!/usr/bin/env python3
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

print("Testing HR imports...")
try:
    from hr.matching_engine import ResumeMatcher
    from hr.sample_data import SAMPLE_RESUMES, SAMPLE_JOB_DESCRIPTIONS
    
    print("✓ HR imports successful")
    
    matcher = ResumeMatcher()
    print("✓ ResumeMatcher initialized")
    
    print(f"✓ Found {len(SAMPLE_RESUMES)} sample resumes")
    print(f"✓ Found {len(SAMPLE_JOB_DESCRIPTIONS)} sample job descriptions")
    
except Exception as e:
    print(f"✗ HR import failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting Job Seeker imports...")
try:
    from job_seeker_pov.models.profile_manager import ProfileManager
    from job_seeker_pov.models.job_analyzer import JobAnalyzer
    from job_seeker_pov.models.resume_generator import ResumeGenerator
    from job_seeker_pov.utils.export_manager import ExportManager
    
    print("✓ Job Seeker imports successful")
    
    pm = ProfileManager()
    ja = JobAnalyzer()
    rg = ResumeGenerator()
    em = ExportManager()
    
    print("✓ All Job Seeker components initialized")
    
except Exception as e:
    print(f"✗ Job Seeker import failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting backend integration imports...")
try:
    from backend.hr_integration import HRIntegration
    from backend.jobseeker_integration import JobSeekerIntegration
    
    print("✓ Backend integration imports successful")
    
    hr_int = HRIntegration()
    js_int = JobSeekerIntegration()
    
    print("✓ Integration components initialized")
    
except Exception as e:
    print(f"✗ Backend integration import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Import Test Complete ===")