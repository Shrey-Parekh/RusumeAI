

-- Create Database
CREATE DATABASE IF NOT EXISTS unified_resume_portal;
USE unified_resume_portal;


-- Table: resumes
-- Stores resume information for HR matching
CREATE TABLE IF NOT EXISTS resumes (
    resume_id INT AUTO_INCREMENT PRIMARY KEY,
    resume_title VARCHAR(255) NOT NULL,
    resume_text LONGTEXT NOT NULL,
    candidate_name VARCHAR(255) NOT NULL,
    candidate_email VARCHAR(255),
    candidate_phone VARCHAR(50),
    experience_years INT,
    current_position VARCHAR(255),
    location VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_resume_title (resume_title),
    INDEX idx_candidate_name (candidate_name),
    INDEX idx_experience_years (experience_years),
    INDEX idx_uploaded_at (uploaded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: job_descriptions
-- Stores job descriptions for HR matching
CREATE TABLE IF NOT EXISTS job_descriptions (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    job_description_text LONGTEXT NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    employment_type ENUM('full-time', 'part-time', 'contract', 'internship') DEFAULT 'full-time',
    experience_required VARCHAR(100),
    salary_range VARCHAR(100),
    location VARCHAR(255),
    posted_by VARCHAR(255),
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('active', 'closed', 'draft') DEFAULT 'active',
    INDEX idx_job_title (job_title),
    INDEX idx_company_name (company_name),
    INDEX idx_department (department),
    INDEX idx_status (status),
    INDEX idx_posted_at (posted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: resume_matches
-- Stores matching results between resumes and job descriptions
CREATE TABLE IF NOT EXISTS resume_matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    job_id INT NOT NULL,
    match_score DECIMAL(5,2) NOT NULL,
    skill_match_percentage DECIMAL(5,2),
    matching_skills JSON,
    missing_skills JSON,
    resume_skills JSON,
    job_skills JSON,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_descriptions(job_id) ON DELETE CASCADE,
    INDEX idx_resume_id (resume_id),
    INDEX idx_job_id (job_id),
    INDEX idx_match_score (match_score),
    INDEX idx_matched_at (matched_at),
    UNIQUE KEY unique_match (resume_id, job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



