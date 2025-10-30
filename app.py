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

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Unified Resume Platform")
    print("="*50)
    print("Server: http://localhost:5000")
    print("="*50 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
