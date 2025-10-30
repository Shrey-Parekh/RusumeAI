"""
Unified Resume Platform - Main Application

This Flask application provides a unified platform for HR professionals and job seekers
to analyze resume-job compatibility using advanced matching algorithms.

Features:
- HR Dashboard: Analyze resume compatibility with job descriptions
- Job Seeker Dashboard: Analyze job descriptions for requirements
- Database integration for storing resumes and job descriptions
- RESTful API endpoints for frontend integration

Routes:
- /: Main landing page
- /hr: HR dashboard interface
- /jobseeker: Job seeker dashboard interface
- /api/hr/*: HR-related API endpoints
- /api/jobseeker/*: Job seeker-related API endpoints
"""

import os
import sys
from flask import Flask, render_template, request, jsonify

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from unified_resume_platform.backend.hr_integration import HRIntegration
    from unified_resume_platform.backend.jobseeker_integration import JobSeekerIntegration
except ImportError as e:
    print(f"Error importing backend modules: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Python path: {sys.path}")
    raise

template_folder = os.path.join(current_dir, 'unified_resume_platform', 'templates')
static_folder = os.path.join(current_dir, 'unified_resume_platform', 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config['SECRET_KEY'] = 'unified-resume-platform-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

hr_integration = HRIntegration()
jobseeker_integration = JobSeekerIntegration()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hr')
def hr_dashboard():
    return render_template('hr_dashboard.html')

@app.route('/jobseeker')
def jobseeker_dashboard():
    return render_template('jobseeker_dashboard.html')

@app.route('/api/hr/match', methods=['POST'])
def hr_match():
    try:
        data = request.get_json()
        result = hr_integration.analyze_match(
            data.get('resume', ''),
            data.get('job_description', '')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/hr/samples')
def hr_samples():
    try:
        result = hr_integration.get_sample_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/hr/sample/<sample_type>/<name>')
def hr_sample_content(sample_type, name):
    try:
        result = hr_integration.get_sample_content(sample_type, name)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/test-db')
def test_database():
    """Test database connection and data for debugging"""
    try:
        from unified_resume_platform.backend.db_manager import DatabaseManager
        db_manager = DatabaseManager()
        
        if db_manager.connect():
            cursor = db_manager.connection.cursor(dictionary=True)
            
            # Test resumes table
            cursor.execute("SELECT COUNT(*) as count FROM resumes")
            resume_count = cursor.fetchone()['count']
            
            # Test job_descriptions table  
            cursor.execute("SELECT COUNT(*) as count FROM job_descriptions")
            job_count = cursor.fetchone()['count']
            
            # Get sample data
            cursor.execute("SELECT resume_id, resume_title, candidate_name FROM resumes LIMIT 3")
            sample_resumes = cursor.fetchall()
            
            cursor.execute("SELECT job_id, job_title, company_name FROM job_descriptions LIMIT 3")
            sample_jobs = cursor.fetchall()
            
            cursor.close()
            db_manager.disconnect()
            
            return jsonify({
                'success': True,
                'message': 'Database connection successful',
                'data': {
                    'resume_count': resume_count,
                    'job_count': job_count,
                    'sample_resumes': sample_resumes,
                    'sample_jobs': sample_jobs
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to connect to database - check password in db_config.py'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}'
        })

@app.route('/api/jobseeker/analyze', methods=['POST'])
def jobseeker_analyze():
    try:
        data = request.get_json()
        result = jobseeker_integration.analyze_job(data.get('job_description', ''))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(_error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(_error):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

def check_database_connection():
    """Check database connection and display status on startup"""
    try:
        from unified_resume_platform.backend.db_config import test_connection
        from unified_resume_platform.backend.db_manager import DatabaseManager
        
        print("\n" + "="*60)
        print("DATABASE CONNECTION CHECK")
        print("="*60)
        
        # Test basic connection
        if test_connection():
            # Test data availability
            db_manager = DatabaseManager()
            if db_manager.connect():
                cursor = db_manager.connection.cursor(dictionary=True)
                
                # Check resumes table
                cursor.execute("SELECT COUNT(*) as count FROM resumes")
                resume_count = cursor.fetchone()['count']
                
                # Check job_descriptions table
                cursor.execute("SELECT COUNT(*) as count FROM job_descriptions")
                job_count = cursor.fetchone()['count']
                
                cursor.close()
                db_manager.disconnect()
                
                print(f"✓ Database: unified_resume_portal")
                print(f"✓ Resumes available: {resume_count}")
                print(f"✓ Job descriptions available: {job_count}")
                
                if resume_count > 0 and job_count > 0:
                    print("✓ Sample data loaded successfully")
                    print("✓ HR dropdowns will be populated")
                else:
                    print("⚠ No sample data found")
                    print("⚠ Please run insert_data.sql to populate database")
                
                return True
            else:
                print("✗ Failed to connect to database")
                return False
        else:
            print("✗ Database connection failed")
            print("\nTo fix this:")
            print("1. Make sure MySQL server is running")
            print("2. Check password in unified_resume_platform/backend/db_config.py")
            print("3. Ensure database 'unified_resume_portal' exists")
            print("4. Run resume.sql and insert_data.sql if needed")
            return False
            
    except Exception as e:
        print(f"✗ Database check error: {e}")
        print("\nApplication will continue but database features may not work")
        return False
    finally:
        print("="*60 + "\n")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Unified Resume Platform")
    print("="*50)
    
    # Check database connection on startup
    db_status = check_database_connection()
    
    print("Server: http://localhost:5000")
    if db_status:
        print("Status: Ready with database")
    else:
        print("Status: Running without database (limited functionality)")
    print("="*50 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
