#!/usr/bin/env python3
import os
import sys

def setup_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    sys.path.insert(0, parent_dir)
    sys.path.insert(0, current_dir)
    
    print(f"Current directory: {current_dir}")
    print(f"Parent directory: {parent_dir}")
    print(f"Python path includes:")
    for path in sys.path[:5]:
        print(f"  - {path}")

def check_imports():
    print("\nChecking imports...")
    
    try:
        from hr.matching_engine import ResumeMatcher
        print("✓ HR matching engine imported successfully")
    except ImportError as e:
        print(f"✗ HR matching engine import failed: {e}")
        return False
    
    try:
        from hr.sample_data import SAMPLE_RESUMES, SAMPLE_JOB_DESCRIPTIONS
        print("✓ HR sample data imported successfully")
    except ImportError as e:
        print(f"✗ HR sample data import failed: {e}")
        return False
    
    try:
        from job_seeker_pov.models.profile_manager import ProfileManager
        print("✓ Job seeker profile manager imported successfully")
    except ImportError as e:
        print(f"✗ Job seeker profile manager import failed: {e}")
        return False
    
    try:
        from job_seeker_pov.models.job_analyzer import JobAnalyzer
        print("✓ Job seeker job analyzer imported successfully")
    except ImportError as e:
        print(f"✗ Job seeker job analyzer import failed: {e}")
        return False
    
    try:
        from job_seeker_pov.models.resume_generator import ResumeGenerator
        print("✓ Job seeker resume generator imported successfully")
    except ImportError as e:
        print(f"✗ Job seeker resume generator import failed: {e}")
        return False
    
    try:
        from job_seeker_pov.utils.export_manager import ExportManager
        print("✓ Job seeker export manager imported successfully")
    except ImportError as e:
        print(f"✗ Job seeker export manager import failed: {e}")
        return False
    
    return True

def main():
    print("=== Unified Resume Platform Startup ===")
    setup_paths()
    
    if not check_imports():
        print("\n❌ Import checks failed. Please check your project structure.")
        return False
    
    print("\n✅ All imports successful. Starting Flask application...")
    
    try:
        from app import app
        print("Flask app imported successfully")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Failed to start Flask app: {e}")
        return False

if __name__ == '__main__':
    main()