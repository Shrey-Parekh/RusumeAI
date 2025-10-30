import json
from datetime import datetime
from .db_config import get_db_connection, close_db_connection

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.db_enabled = True

    def connect(self):
        """Connect to database, returns True if successful"""
        try:
            self.connection = get_db_connection()
            if self.connection is None:
                self.db_enabled = False
                print("⚠ Database disabled - running without database storage")
                return False
            return True
        except Exception as e:
            print(f"⚠ Database connection failed: {e}")
            self.db_enabled = False
            return False

    def disconnect(self):
        """Safely disconnect from database"""
        try:
            close_db_connection(self.connection)
            self.connection = None
        except Exception as e:
            print(f"Warning: Error disconnecting from database: {e}")

    def save_resume(self, resume_text, candidate_name=None, candidate_email=None):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                INSERT INTO resumes (resume_text, candidate_name, candidate_email)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (resume_text, candidate_name, candidate_email))
            self.connection.commit()
            resume_id = cursor.lastrowid
            cursor.close()

            self.log_audit('resume_upload', 'resume', resume_id, candidate_email)
            return resume_id
        except Exception as e:
            print(f"Error saving resume: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def save_job_description(self, job_title, company_name, job_description_text, posted_by=None):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                INSERT INTO job_descriptions (job_title, company_name, job_description_text, posted_by)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (job_title, company_name, job_description_text, posted_by))
            self.connection.commit()
            job_id = cursor.lastrowid
            cursor.close()

            self.log_audit('job_post', 'job_description', job_id, posted_by)
            return job_id
        except Exception as e:
            print(f"Error saving job description: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def save_resume_match(self, resume_id, job_id, match_score, skill_match_percentage, match_details):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()

            match_query = """
                INSERT INTO resume_matches (resume_id, job_id, match_score, skill_match_percentage)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    match_score = VALUES(match_score),
                    skill_match_percentage = VALUES(skill_match_percentage),
                    matched_at = CURRENT_TIMESTAMP
            """
            cursor.execute(match_query, (resume_id, job_id, match_score, skill_match_percentage))
            self.connection.commit()

            match_id_query = "SELECT match_id FROM resume_matches WHERE resume_id = %s AND job_id = %s"
            cursor.execute(match_id_query, (resume_id, job_id))
            match_id = cursor.fetchone()[0]

            details_query = """
                INSERT INTO match_details (match_id, matching_skills, missing_skills, resume_skills, job_skills)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    matching_skills = VALUES(matching_skills),
                    missing_skills = VALUES(missing_skills),
                    resume_skills = VALUES(resume_skills),
                    job_skills = VALUES(job_skills),
                    created_at = CURRENT_TIMESTAMP
            """
            cursor.execute(details_query, (
                match_id,
                json.dumps(match_details.get('matching_skills', [])),
                json.dumps(match_details.get('missing_skills', [])),
                json.dumps(match_details.get('resume_skills', [])),
                json.dumps(match_details.get('jd_skills', []))
            ))
            self.connection.commit()
            cursor.close()

            self.log_audit('match_analysis', 'resume_match', match_id, None)
            return match_id
        except Exception as e:
            print(f"Error saving resume match: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def save_job_analysis(self, job_description_text, analysis_data):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                INSERT INTO job_analysis (
                    job_description_text, keywords, required_skills, preferred_skills,
                    experience_level, education_requirements
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                job_description_text,
                json.dumps(analysis_data.get('keywords', [])),
                json.dumps(analysis_data.get('required_skills', [])),
                json.dumps(analysis_data.get('preferred_skills', [])),
                analysis_data.get('experience_level', ''),
                analysis_data.get('education_requirements', '')
            ))
            self.connection.commit()
            analysis_id = cursor.lastrowid
            cursor.close()

            self.log_audit('job_analysis', 'job_analysis', analysis_id, None)
            return analysis_id
        except Exception as e:
            print(f"Error saving job analysis: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def save_skill(self, skill_name, skill_category=None):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                INSERT INTO skills (skill_name, skill_category)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE skill_id=LAST_INSERT_ID(skill_id)
            """
            cursor.execute(query, (skill_name, skill_category))
            self.connection.commit()
            skill_id = cursor.lastrowid
            cursor.close()
            return skill_id
        except Exception as e:
            print(f"Error saving skill: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def link_resume_skill(self, resume_id, skill_id, proficiency_level='intermediate'):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                INSERT INTO resume_skills (resume_id, skill_id, proficiency_level)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE proficiency_level = VALUES(proficiency_level)
            """
            cursor.execute(query, (resume_id, skill_id, proficiency_level))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error linking resume skill: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def link_job_skill(self, job_id, skill_id, is_required=True, importance_level='medium'):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                INSERT INTO job_skills (job_id, skill_id, is_required, importance_level)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    is_required = VALUES(is_required),
                    importance_level = VALUES(importance_level)
            """
            cursor.execute(query, (job_id, skill_id, is_required, importance_level))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error linking job skill: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def get_resume_matches(self, resume_id=None, job_id=None, min_score=None):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT rm.*, r.candidate_name, r.candidate_email,
                       j.job_title, j.company_name,
                       md.matching_skills, md.missing_skills
                FROM resume_matches rm
                JOIN resumes r ON rm.resume_id = r.resume_id
                JOIN job_descriptions j ON rm.job_id = j.job_id
                LEFT JOIN match_details md ON rm.match_id = md.match_id
                WHERE 1=1
            """
            params = []

            if resume_id:
                query += " AND rm.resume_id = %s"
                params.append(resume_id)
            if job_id:
                query += " AND rm.job_id = %s"
                params.append(job_id)
            if min_score:
                query += " AND rm.match_score >= %s"
                params.append(min_score)

            query += " ORDER BY rm.match_score DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting resume matches: {e}")
            return []

    def get_job_analyses(self, limit=10):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT * FROM job_analysis
                ORDER BY analyzed_at DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting job analyses: {e}")
            return []

    def log_audit(self, action_type, entity_type, entity_id, performed_by):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                INSERT INTO audit_log (action_type, entity_type, entity_id, performed_by)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (action_type, entity_type, entity_id, performed_by))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error logging audit: {e}")
            return False
