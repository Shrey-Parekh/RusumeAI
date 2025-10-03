# app.py
from flask import Flask, render_template, request, jsonify
from matching_engine import ResumeMatcher
from sample_data import SAMPLE_RESUMES, SAMPLE_JOB_DESCRIPTIONS
import os

app = Flask(__name__)
matcher = ResumeMatcher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match_resume():
    try:
        data = request.get_json()
        resume_text = data.get('resume', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Resume and job description are required'}), 400
        
        analysis = matcher.get_match_analysis(resume_text, job_description)
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/samples', methods=['GET'])
def get_samples():
    """Get sample resumes and job descriptions"""
    return jsonify({
        'resumes': list(SAMPLE_RESUMES.keys()),
        'job_descriptions': list(SAMPLE_JOB_DESCRIPTIONS.keys())
    })

@app.route('/sample/<type>/<name>', methods=['GET'])
def get_sample(type, name):
    """Get specific sample resume or job description"""
    if type == 'resume':
        return jsonify({'content': SAMPLE_RESUMES.get(name, '')})
    elif type == 'job_description':
        return jsonify({'content': SAMPLE_JOB_DESCRIPTIONS.get(name, '')})
    else:
        return jsonify({'error': 'Invalid type'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)