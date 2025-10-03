from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import json
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

try:
    from backend.hr_integration import HRIntegration
    from backend.jobseeker_integration import JobSeekerIntegration
except ImportError as e:
    print(f"Error importing backend modules: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Parent directory: {parent_dir}")
    print(f"Python path: {sys.path}")
    raise

app = Flask(__name__)
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
    profile = jobseeker_integration.get_profile()
    return render_template('jobseeker_dashboard.html', profile=profile)

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

@app.route('/api/jobseeker/profile', methods=['GET', 'POST', 'PUT'])
def jobseeker_profile():
    try:
        if request.method == 'GET':
            result = jobseeker_integration.get_profile()
        elif request.method == 'POST':
            data = request.get_json()
            result = jobseeker_integration.create_profile(data)
        elif request.method == 'PUT':
            data = request.get_json()
            result = jobseeker_integration.update_profile(data)
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

@app.route('/api/jobseeker/generate', methods=['POST'])
def jobseeker_generate():
    try:
        data = request.get_json()
        result = jobseeker_integration.generate_resume(
            data.get('profile'),
            data.get('analysis')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/export', methods=['POST'])
def jobseeker_export():
    try:
        data = request.get_json()
        result = jobseeker_integration.export_resume(
            data.get('content', ''),
            data.get('format', 'txt'),
            data.get('profile'),
            data.get('job_description')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/history')
def jobseeker_history():
    try:
        result = jobseeker_integration.get_history()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/validate', methods=['POST'])
def jobseeker_validate():
    try:
        data = request.get_json()
        result = jobseeker_integration.validate_profile(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)